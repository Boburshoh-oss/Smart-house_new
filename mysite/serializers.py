from asyncio.log import logger
from rest_framework import serializers
from .models import Channel, Device, Home, Product, Sensor
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    
    def update(self, instance, validated_data):
        my_request = validated_data.get('state', None)
        my_topic = validated_data.get('topic_name', instance.topic_name)

        if my_request is True:
            message = 'on'
        elif my_request is False:
            message = 'off'

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("my.group", {"type": "publish.results", "text":message,'topic':my_topic})

        instance.state = validated_data.get('state', instance.state)
        instance.save()
        return instance

    def create(self, validated_data):
        product_abilty = validated_data['device'].product.num_of_channels
        device = validated_data['device'].channels.all()
        channels_count = device.count()
        if channels_count < product_abilty:
            return super().create(validated_data)
        raise serializers.ValidationError({"channels maximum count must be":product_abilty})