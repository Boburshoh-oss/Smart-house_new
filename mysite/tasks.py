
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
    print("11111111")
    client.connect('localhost',1883,60)
    print("222222")
    print(channels,"eeeeeee channels")
    for chan in channels:
        topic_name = Channel.objects.get(id=chan)
        print("33333")
        client.publish(topic_name.topic_name,status)
        time.sleep(1)
        print("444444")
    client.disconnect()
    return {"result":True}
