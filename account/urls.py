from django.urls import path
from .views import *
urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('me/', OwnUserView.as_view()),
    path('me/<int:pk>/', UserDetailUpdateView.as_view()),
]