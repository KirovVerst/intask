from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer


# Create your views here.

class UserListAPIView(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

	def get_permissions(self):
		if self.request.method in permissions.SAFE_METHODS:
			return [permissions.IsAuthenticated(), ]
		return [permissions.AllowAny(), ]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()
