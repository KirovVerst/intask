from django.shortcuts import render
from rest_framework import generics
from serializers import NotificationSerializer
from models import Notification


# Create your views here.

class NotificationCreateListAPIView(generics.ListCreateAPIView):
	serializer_class = NotificationSerializer
	queryset = Notification.objects.all()
