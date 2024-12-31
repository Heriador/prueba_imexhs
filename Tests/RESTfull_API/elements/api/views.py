from rest_framework.response import Response
from rest_framework import status, viewsets
from elements.models import Element
from django.http import Http404
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
        logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")
        data = dict(request.data)
        elements_data = []
        try:
            # iterate over the data and create a new device and element
            for device_data in data.values():

                # transform the data to the device model
                data_device = self.__transform_element_data(device_data)
                
                # serialize the device data
                serializer = DeviceSerializer(data=data_device)

                # check if the data is valid
                if serializer.is_valid():
                    # save the device data
                    serializer.save()

                    # normalize the data and serialize it
                    element_data = self.__get_normalized_data(serializer.data)
                    element_serializer = self.get_serializer(data=element_data)

                    # check if the data is valid
                    if element_serializer.is_valid():
                        # save the element data
                        element_serializer.save()

                        # append the element data to the elements_data list to return it
                        elements_data.append(element_serializer.data)
                    else:

                        #Logging the validation error is the data is not valid and return the error
                        logger.error(f"Validation error: {element_serializer.errors} ")
                        return Response(element_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    #Logging the validation error is the data is not valid and return the error
                    logger.error(f"Validation error: {serializer.errors} ")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            #Logging the created elements data and return it
            logger.info(f"created new elements info: {elements_data}")
            return Response(elements_data, status=status.HTTP_201_CREATED)
        
        #Logging the error if any exception is raised
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
    
    def destroy(self, request, *args, **kwargs):
        
        logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")


        instance = self.get_object()
        device = instance.device
        id = device.id

        instance.delete()
        device.delete()

        logger.info(f"Deleted element: {instance}")
        return Response({"message": f"element {id} deleted successfully"},status=status.HTTP_200_OK)
        
        
    def update(self, request, *args, **kwargs):
        logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")

        instance = self.get_object()
        device_data = request.data.get('device', {})
        device = instance.device
        old_device_id = device.id

        if len(device_data) == 0:
            return Response({"message": "No data to update"}, status=status.HTTP_400_BAD_REQUEST)

        # update device id if passed in the request
        if 'id'in device_data:
            device.id = device_data['id']

        # update device name if passed in the request
        if 'device_name' in device_data:
            device.device_name = device_data['device_name']

        # save the updated device
        device.save()

        # update the element device id
        Element.objects.filter(device=old_device_id).update(device=device.id)
        
        
        serializer = self.get_serializer(instance)

        logger.info(f"Updated element: {serializer.data}")
    
        return Response(serializer.data,status=status.HTTP_200_OK)
    
        
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
 
    # Transform the data to the device model
    def __transform_element_data(self,data):
        
        device = dict()

        device['id'] = data['id']
        device['device_name'] = data['deviceName']
        device['data'] = self.__extract_numbers_data(data['data'])

        return device

    # Extract the numbers from the data and return them
    def __extract_numbers_data(self,data):
        extracted_numbers = []
        
        for item in data:
            extracted_numbers.extend(item.split(' '))

        return extracted_numbers
    
    # Normalize the data
    def __get_normalized_data(self,device):
        element_data = dict()

        #Normzalizing the data in the element
        max_data_value = max(device['data'])
        data_normalized = [round(int(item)/max_data_value,4) for item in device['data']]
        
        #Calculating the average of the data before and after normalization
        average_before_normalization = sum(device['data'])/len(device['data'])
        average_after_normalization = sum(data_normalized)/len(data_normalized)

        #Adding the data to the element data
        element_data['device'] = device['id']
        element_data['average_before_normalization'] = round(average_before_normalization,4)
        element_data['average_after_normalization'] = round(average_after_normalization,4)
        element_data['data_size'] = len(device['data'])

        return element_data
