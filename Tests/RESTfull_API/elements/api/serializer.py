from rest_framework import serializers
from elements.models import Element, Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'device_name', 'data')

class ElementSerializer(serializers.ModelSerializer):

    source_device = DeviceSerializer(read_only=True, source='device')

    class Meta:
        model = Element
        fields = '__all__'



