
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import dateformat
import time
from config.celery import app
from mysite.models import Channel

client = mqtt.Client()
client.username_pw_set(username="bobur",password="bobur")

@app.task() 
def mqtt_task_scheduale(status,channels,sensor_status=None):
    client.connect('localhost',1883,60)
    for chan in channels:
        channel = Channel.objects.get(id=chan)
        client.publish(channel.topic_name,status)
        time.sleep(1)
    client.disconnect()
    return {"result":True}
