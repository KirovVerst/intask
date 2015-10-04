from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from models import CustomUser
from serializers import UserSerializer


# Create your views here.

class UserListAPIView(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()