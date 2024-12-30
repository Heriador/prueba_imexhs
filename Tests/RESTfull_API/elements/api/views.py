from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from elements.models import Device, Element
from .serializer import ElementSerializer, DeviceSerializer
from .filters import ElementFilter
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger('django')
logger.addHandler('file')     

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    http_method_names = ['get', 'post', 'put', 'patch' ,'delete']
    filterset_class = ElementFilter
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'device__id'

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        elements_data = []
        try:

            for device_data in data.values():
                data_device = self.__transform_element_data(device_data)
                serializer = DeviceSerializer(data=data_device)

                if serializer.is_valid():
                    serializer.save()
                    element_data = self.__get_normalized_data(serializer.data)
                    element_serializer = self.get_serializer(data=element_data)

                    if element_serializer.is_valid():
                        element_serializer.save()

                        elements_data.append(element_serializer.data)
                    else:
                        logger.error(f"Validation error: {element_serializer.errors} ")
                        return Response(element_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    logger.error(f"Validation error: {serializer.errors} ")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"created new elements info: {elements_data}")
            return Response(elements_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error: {e} ")
            return Response(e['message'])

    def list(self, request, *args, **kwargs):
        logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)


        logger.info(f"List all elements: {serializer.data}")
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")

        element = self.get_object()
        serializer = self.get_serializer(element)
        logger.info(f"Response element: {serializer.data}")
        return Response(serializer.data)
    
    def __transform_element_data(self,data):
        
        device = dict()

        device['id'] = data['id']
        device['device_name'] = data['deviceName']
        device['data'] = self.__extract_numbers_data(data['data'])

        return device

    def __extract_numbers_data(self,data):
        extracted_numbers = []
        
        for item in data:
            extracted_numbers.extend(item.split(' '))

        return extracted_numbers
    
    def __get_normalized_data(self,device):
        element_data = dict()

        max_data_value = max(device['data'])
        data_normalized = [round(int(item)/max_data_value,4) for item in device['data']]
        
        average_before_normalization = sum(device['data'])/len(device['data'])
        average_after_normalization = sum(data_normalized)/len(data_normalized)

        element_data['device'] = device['id']
        element_data['average_before_normalization'] = round(average_before_normalization,4)
        element_data['average_after_normalization'] = round(average_after_normalization,4)
        element_data['data_size'] = len(device['data'])

        return element_data
