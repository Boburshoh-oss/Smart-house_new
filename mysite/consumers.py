import json
from mqttasgi.consumers import MqttConsumer
from asgiref.sync import sync_to_async
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from .models import Channel, Sensor, Sensor_cache
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
            payload = mqtt_message['payload'].decode("utf-8") 
            channel = await Channel.objects.aget(topic_name=mqtt_message['topic'])
            match payload:
                case '1':
                    channel.state = 'on'
                    await sync_to_async(channel.save)()
                case '0':
                    channel.state = 'off'
                    await sync_to_async(channel.save)()
            


            await self.unsubscribe(mqtt_message['topic'])
        pass
    
    async def publish_results(self, event):
        data = event['text']
        topic = event['topic']
        print(data,topic,'publish done')
        await self.publish(str(topic), data, qos=2, retain=False)

    async def my_custom_message(self, event):
        print(event)
        data = event['text']
        print('subscribe a topic')
        await self.subscribe(data, 2)
        
    async def disconnect(self):
        await self.unsubscribe('my/testing/topic')

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))