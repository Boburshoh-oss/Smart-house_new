import json
from datetime import datetime
from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .models import Home, Sensor, SmartCondition
from .tasks import mqtt_task_scheduale


@receiver(post_save, sender=Home)
def create_home_topic(sender, instance, created, **kwargs):  # type: ignore
    if created:
        instance.key = f"{uuid4()}{instance.id}"
        instance.save()

@receiver(post_save, sender=Sensor)
def request_to_mqtt(sender, instance, created, **kwargs):   # type: ignore
    if created:
        my_topic = instance.topic_name
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("my.group", {"type": "my.custom.message", "text":str(my_topic)}) # type: ignore

@receiver(post_delete, sender=Sensor)
def unsubscribe_topic(sender, instance, **kwargs):
        my_topic = instance.topic_name
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("my.group", {"type": "unsubscribe_sensors", "topic":str(my_topic)}) # type: ignore

@receiver(post_save, sender=SmartCondition)
def create_sm(sender, instance, created, **kwargs):
        print("ishlaydi")
        timer = instance.condition.timer
        hour = timer.strftime("%H")
        minute = timer.strftime("%M")
        channels_id = []
        for chan in instance.channel.all():
            channels_id.append(chan.id)
            
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=str(minute),
            hour=str(hour),
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
        PeriodicTask.objects.create(
            crontab=schedule,                  # we created this above.
            name=str(uuid4()),          # simply describes this periodic task.
            task='mysite.tasks.mqtt_task_scheduale',  # name of task.
            args=json.dumps([instance.status, channels_id]),
            
        )
# @receiver(post_save, sender=SmartCondition)
# def request_to_mqtt(sender, instance, created, **kwargs):
#     channels = instance.channel.all()
#     channels_id = []
    
#     for i in channels:
#         channels_id.append(i.id)
#     status = instance.status
#     hour = instance.condition.timer.strftime("%H")
#     minute = instance.condition.timer.strftime("%M")
#     second = instance.condition.timer.strftime("%S")
    
    
#     now_time = datetime.now()  # type: ignore
#     target_time = now_time.replace(hour=int(hour), minute=int(minute), second=int(second))
    
#     sensor_status = instance.condition.sensor_status
#     mqtt_task_scheduale.apply_async((f"{status}",channels_id,None), eta=target_time)
    
    # async_to_sync(channel_layer.group_send)("my.group", {"type": "my.custom.message", "text":str(my_topic)})

        