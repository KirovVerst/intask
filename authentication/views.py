# coding=utf-8
from rest_framework import generics, permissions, validators, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from serializers import AuthCustomTokenSerializer, validate_email
from users.serializers import UserSerializer
from django.contrib.auth.models import User, Group


# Create your views here.

class ObtainAuthToken(APIView):
	"""
	Return a user with his token.
	"""
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (FormParser, MultiPartParser, JSONParser,)

	renderer_classes = (JSONRenderer,)

	def post(self, request):
		serializer = AuthCustomTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)

		data = UserSerializer(instance=user).to_representation(instance=user)
		data['token'] = unicode(token.key)

		return Response(data)
