
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import dateformat

from config.celery import app
from mysite.models import Channel


@app.task() 
def mqtt_task_scheduale(status,channels,sensor_status):
    channel_layer = get_channel_layer()
    for chan in channels:
        topic_name = Channel.objects.get(id=chan)
        async_to_sync(channel_layer.group_send)("my.group", {"type": "publish.results", "text":'suka ishlayapsanmi',"topic":str('fuck')}) # type: ignore
    # if sensor_status:
    #     for sensor in sensor_status:
    #         async_to_sync(channel_layer.group_send)("my.group", {"type": "publish.results", "text":status,"topic":str(sensor.topic_name)})
    return {"result":True}