from django.core.management.base import BaseCommand, CommandError
from mysite.models import Sensor
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):

    def handle(self, *args, **options):
        # ...
        sensors = Sensor.objects.all()
        for sensor in sensors:
                print('ishlavottimi')
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)("my.group", {"type": "my.custom.message", "text":str(sensor.topic_name)})
        pass