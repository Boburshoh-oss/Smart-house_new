
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import dateformat

from config.celery import app
from mysite.models import Channel

client = mqtt.Client()

@app.task() 
def mqtt_task_scheduale(status,channels,sensor_status=None):
    print("11111111")
    client.connect('localhost',1883,60)
    print("222222")
    print(channels,"eeeeeee channels")
    for chan in channels:
        topic_name = Channel.objects.get(id=chan)
        print("33333")
        client.publish(topic_name.topic_name,status)
        print("444444")
        # async_to_sync(channel_layer.group_send)("my.group", {"type": "publish","topic":str('fuck'),"payload":status}) # type: ignore
    # if sensor_status:
    #     for sensor in sensor_status:
    #         async_to_sync(channel_layer.group_send)("my.group", {"type": "publish.results", "text":status,"topic":str(sensor.topic_name)})
    return {"result":True}