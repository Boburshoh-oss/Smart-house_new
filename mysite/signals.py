from uuid import uuid4
from .models import Home, Sensor
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Home)
def create_home_topic(sender, instance, created, **kwargs):
    if created:
        instance.key = f"{uuid4()}{instance.id}"
        instance.save()

@receiver(post_save, sender=Sensor)
def request_to_mqtt(sender, instance, created, **kwargs):
    if created:
        my_topic = instance.topic_name
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("my.group", {"type": "my.custom.message", "text":str(my_topic)})

# @receiver(post_delete, sender=Sensor)
# def unsubscribe_topic(sender, instance, **kwargs):
#         my_topic = instance.topic_name
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)("my.group", {"type": "unsubscribe", "text":str(my_topic)})


        