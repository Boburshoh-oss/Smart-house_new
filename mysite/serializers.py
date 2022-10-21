from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Channel, Device, Home, Product, Sensor, Sensor_cache, SmartCondition, Condition, SensorState, Description


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id','owner','name','device','state','created_at','type']
        read_only_fields = ('owner','created_at','updated_at')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DeviceSerializer(serializers.ModelSerializer):
    channels = serializers.PrimaryKeyRelatedField(many=True, queryset=Channel.objects.all(),required=False)
    sensors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sensor.objects.all(),required=False)
        
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('owner','channels','sensors')

class DevicePutSerializer(serializers.ModelSerializer):
    
    channels = serializers.PrimaryKeyRelatedField(many=True, queryset=Channel.objects.all(),required=False)
    sensors = serializers.PrimaryKeyRelatedField(many=True, queryset=Sensor.objects.all(),required=False)
    
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('owner','channels','sensors','home','name')

class HomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Home
        fields = "__all__"
        read_only_fields = ('created_at','owner','key')
    

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id','owner','name','device','state','created_at','topic_name']
        read_only_fields = ('id', 'created_at','owner')
    

    def create(self, validated_data):
        product_abilty = validated_data['device'].product.num_of_channels
        device = validated_data['device'].channels.all()
        channels_count = device.count()
        if channels_count < product_abilty:
            return super().create(validated_data)
        raise serializers.ValidationError({"channels maximum count must be":product_abilty})


class SensorStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorState
        fields = '__all__'

class Sensor_cacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor_cache
        fields = '__all__'

class ConditionSerializer(WritableNestedModelSerializer):
    timer=serializers.TimeField(format='%H:%M',default=None)  # type: ignore
    sensor_status = SensorStateSerializer(default=None)
    class Meta:
        model = Condition
        fields = '__all__'
        
class SmartConditionSerializer(WritableNestedModelSerializer):
    condition = ConditionSerializer()
    class Meta:
        model = SmartCondition
        fields = '__all__'
        read_only_fields = ('id', 'created_at','owner')

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'
        read_only_fields = ('id', 'created_at','owner')