from .models import Channel, Sensor, Sensor_cache
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import os

import django
from asgiref.sync import sync_to_async
from mqttasgi.consumers import MqttConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


class MyMqttConsumer(MqttConsumer):

    async def connect(self):
        await self.subscribe('my/testing/topic', 2)
        await self.subscribe('my/testing/topic2', 2)        
        await self.channel_layer.group_add("my.group", self.channel_name)# type: ignore

    async def receive(self, mqtt_message):
        print('Received a message at topic:', mqtt_message['topic'])
        print('With payload', mqtt_message['payload'])
        print('And QOS:', mqtt_message['qos'])
        try:
            sensor = await Sensor.objects.aget(topic_name=mqtt_message['topic'])
            data = str(mqtt_message['payload'].decode("utf-8"))
            await Sensor_cache.objects.acreate(sensor=sensor, state=data)

        except:
            payload = mqtt_message['payload'].decode("utf-8")
            try:
                channel = await Channel.objects.aget(topic_name=mqtt_message['topic'])
                match payload:
                    case '1':
                        channel.state = 'on'
                        await sync_to_async(channel.save)()
                    case '0':
                        channel.state = 'off'
                        await sync_to_async(channel.save)()
                await self.unsubscribe(mqtt_message['topic'])
            except:
                await self.unsubscribe(mqtt_message['topic'])
        pass

    async def publish_results(self, event):

        data = event['text']
        topic = event['topic']
        print(data, topic, 'publish done')
        await self.publish(str(topic), data, qos=1, retain=False)

    async def my_custom_message(self, event):
        print(event)
        data = event['text']
        print('subscribe a topic')
        if data not in self.subscribed_topics:
            await self.subscribe(data, 2)
            
    async def unsubscribe_sensors(self,event):
        topic = event['topic']
        print("unsubscribe topic: "+topic)
        await self.unsubscribe(topic)
        
    async def disconnect(self):
        await self.unsubscribe('my/testing/topic')


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']
        self.room_group_name = 'my_gorup'

        # Join room group
        await self.channel_layer.group_add(  # type: ignore
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(  # type: ignore
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # print(text_data,"binary data")
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(  # type: ignore
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )  # type: ignore

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        # await self.send(text_data={
        #     'message': message
        # })
