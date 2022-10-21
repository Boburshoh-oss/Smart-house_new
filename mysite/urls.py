from django.urls import include, path
from rest_framework import routers

from .views import *
from .views import index, room

router = routers.DefaultRouter()

router.register('product', ProductViewSet)
urlpatterns = [
    path('', index, name='index'),
    path('client/',index_client),
    path('chat/<str:room_name>/', room, name='room'),
    path('product', include(router.urls)),
    path('home/', HomeListCreateAPIView.as_view()),
    path('home/<int:pk>/', HomeDetailAPIView.as_view()),
    path('channel/', ChannelListCreateAPIView.as_view()),
    path('channel/<int:pk>/', ChannelDetailAPIView.as_view()),
    path('device/', DeviceListCreateAPIView.as_view()),
    path('device/<int:pk>/', DeviceDetailAPIView.as_view()),
    path('sensor/', SensorListCreateAPIView.as_view()),
    path('sensor_cache/', SensorCacheListAPIView.as_view()),
    path('sensor/<int:pk>/', SensorDetailAPIView.as_view()),
    path('smartconditions/', SmartConditionListCreateApiView.as_view()),
    path('smartconditions/<int:pk>/', SmartConditionRetrieveApiView.as_view()),
    # path('product/', ProductViewSet.as_view()),
    
    path('description/',DescriptionListCreateApiView.as_view())
]
