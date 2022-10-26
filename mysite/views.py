from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Channel, Device, Home, Product, Sensor, SmartCondition, Description, Sensor_cache
from .serializers import (ChannelSerializer, DevicePutSerializer,
                          DeviceSerializer, HomeSerializer, ProductSerializer,
                          SensorSerializer, SmartConditionSerializer,
                          Sensor_cacheSerializer,DescriptionSerializer)

# Create your views here.
client = mqtt.Client()
client.username_pw_set(username="bobur",password="bobur")

def index(request):
    return render(request, 'chat/index.html')


def index_client(request):
    return render(request, 'client.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def index1(request):
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("my.group", {  # type: ignore
        "type": "publish.results", "text": "6", 'topic': 'Myhome9b054ad1-4f70-4439-bcd1-43df034a74a71/mydevice/lamp11'})

    return HttpResponse('hello world')


class ChannelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Channel.objects.filter(owner=user)
        else:
            queryset = Channel.objects.all()
        return queryset


class ChannelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()


class DeviceListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Device.objects.filter(owner=user)
        else:
            queryset = Device.objects.all()
        return queryset


class DeviceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DevicePutSerializer
    queryset = Device.objects.all()


class HomeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = HomeSerializer
    queryset = Home.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Home.objects.filter(owner=user)
        else:
            queryset = Home.objects.all()
        return queryset


class HomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = HomeSerializer
    queryset = Home.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class SensorListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Sensor.objects.filter(owner=user)
        else:
            queryset = Sensor.objects.all()
        return queryset


class SensorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()

class SensorCacheListAPIView(generics.ListAPIView):
    serializer_class = Sensor_cacheSerializer
    queryset = Sensor_cache.objects.all()

class SmartConditionListCreateApiView(generics.ListCreateAPIView):
    serializer_class = SmartConditionSerializer
    queryset = SmartCondition.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = SmartCondition.objects.filter(owner=user)
        else:
            queryset = SmartCondition.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)


class SmartConditionRetrieveApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SmartConditionSerializer
    queryset = SmartCondition.objects.all()


class DescriptionListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DescriptionSerializer
    queryset = Description.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)
