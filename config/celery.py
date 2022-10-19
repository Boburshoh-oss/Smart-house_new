import os

# django.setup()
from celery import Celery

# from core.task import mqtt_task_scheduale
# from core.models.condition import SmartCondition
# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


app = Celery('config')  # type: ignore

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, mqtt_task_scheduale.s(), name='check every 60')
# # Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.conf.beat_schedule = {
#     'check every 60': {
#         'task': 'core.tasks.mqtt_task_scheduale',
#         'schedule': 30.0,
#     },
# }
app.conf.timezone = 'Asia/Tashkent'  # type: ignore
app.config_from_object('django.conf:settings', namespace='CELERY')



# Load task modules from all registered Django apps.
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')