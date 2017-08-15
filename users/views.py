from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import parsers, permissions, viewsets, mixins
from users.serializers import UserSerializer
from users.permissions import CanRetrieveUpdateDestroyUser


# Create your views here.


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [parsers.JSONParser]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny(), ]
        return [permissions.IsAuthenticated(), CanRetrieveUpdateDestroyUser(), ]
