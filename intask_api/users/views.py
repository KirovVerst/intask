from django.contrib.auth.models import User
from rest_framework import parsers, permissions, viewsets, mixins
from users.serializers import UserSerializer
from users.permissions import CanRetrieveUpdateDestroyUser
from users.tasks import send_message


# Create your views here.


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny(), ]
        return [permissions.IsAuthenticated(), CanRetrieveUpdateDestroyUser(), ]

    def create(self, request, *args, **kwargs):
        r = super(UserViewSet, self).create(request, args, kwargs)
        data = {
            'subject': 'Intask | New user',
            'text': 'New user \'{}\' has been registered.'.format(request.data.get('email', ''))
        }
        send_message.delay(**data)
        return r
