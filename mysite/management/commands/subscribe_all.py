from django.core.management.base import BaseCommand, CommandError
from mysite.models import Sensor
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

async def subscribe_sensors():
    async for sensor in Sensor.objects.all():
        print('ishlavottimi')
        channel_layer = get_channel_layer()  # type: ignore
        await channel_layer.group_send("my.group", {"type": "my.custom.message", "text":str(sensor.topic_name)}) # type: ignore

class Command(BaseCommand):

    def handle(self, *args, **options):
        async_to_sync(subscribe_sensors)()