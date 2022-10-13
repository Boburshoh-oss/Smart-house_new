from django.shortcuts import render
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from .models import User
from rest_framework import generics,views
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserRegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OwnUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        profile = User.objects.filter(username=self.request.user.username)
        return profile
    
class UserLoginView(views.APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class Logout(views.APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login_view")