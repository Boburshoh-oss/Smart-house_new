import json
from mqttasgi.consumers import MqttConsumer
from django.conf import settings
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from .models import Sensor, Sensor_cache
from channels.generic.websocket import AsyncWebsocketConsumer
class MyMqttConsumer(MqttConsumer):

    async def connect(self):
        await self.subscribe('my/testing/topic', 2)
        await self.subscribe('my/testing/topic2', 2)
        await self.channel_layer.group_add("my.group", self.channel_name)

    async def receive(self, mqtt_message):
        print('Received a message at topic:', mqtt_message['topic'])
        print('With payload', mqtt_message['payload'])
        print('And QOS:', mqtt_message['qos'])
        try:
            sensor = await Sensor.objects.aget(topic_name=mqtt_message['topic'])
            data=str(mqtt_message['payload'].decode("utf-8"))
            await Sensor_cache.objects.acreate(sensor=sensor,state=data)
        except:
            await self.unsubscribe(mqtt_message['topic'])
        pass
    
    async def publish_results(self, event):
        print("kirrrrr")
        data = event['text']
        topic = event['topic']
        print(data,topic,'publish boldimi')
        await self.publish(str(topic), data, qos=2, retain=False)

    async def my_custom_message(self, event):
        print('Received a channel layer message')
        print(event)
        data = event['text']
        await self.subscribe(data, 2)
        
    async def disconnect(self):
        await self.unsubscribe('my/testing/topic')

