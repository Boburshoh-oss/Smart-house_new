from django.urls import path,include
from .views import index
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()

router.register('product', ProductViewSet)
urlpatterns = [
    path('index',index),
    path('', include(router.urls)),
    path('home/', HomeListCreateAPIView.as_view()),
    path('home/<int:pk>/', HomeDetailAPIView.as_view()),
    path('channel/', ChannelListCreateAPIView.as_view()),
    path('channel/<int:pk>/', ChannelDetailAPIView.as_view()),
    path('device/', DeviceListCreateAPIView.as_view()),
    path('device/<int:pk>/', DeviceDetailAPIView.as_view()),
    path('sensor/', SensorListCreateAPIView.as_view()),
    path('sensor/<int:pk>/', SensorDetailAPIView.as_view()),
    # path('smartconditions/', SmartConditionListCreateApiView.as_view()),
    # path('smartconditions/<int:pk>/', SmartConditionRetrieveApiView.as_view()),
    # path('product/', ProductViewSet.as_view()),
    
    # path('description/',DescriptionListCreateApiView.as_view())
]
