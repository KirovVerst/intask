from django.shortcuts import render
from rest_framework import generics
from serializers import CustomUser


# Create your views here.

class CustomUserListAPIView(generics.ListCreateAPIView):
	serializer_class = CustomUser
	queryset = CustomUser.objects.all()
