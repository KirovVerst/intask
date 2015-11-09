# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, validators, exceptions
from rest_framework.authtoken.models import Token


def validate_email(email):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(email)
		return True
	except ValidationError:
		return False


class AuthCustomTokenSerializer(serializers.Serializer):
	email = serializers.CharField()
	password = serializers.CharField()

	def validate(self, attrs):
		email = attrs.get('email')
		password = attrs.get('password')

		if email and password:
			# Check if user sent email
			if validate_email(email):

				if len(User.objects.filter(email=email)) == 0:
					msg = 'User with this email does not exist.'
					raise exceptions.ValidationError(msg)
				user = authenticate(username=email, password=password)

			else:
				msg = 'Email is not valid.'
				raise exceptions.ValidationError(msg)

			if user:
				if not user.is_active:
					msg = 'User account is disabled.'
					raise exceptions.ValidationError(msg)
			else:
				msg = 'Password is not correct.'
				raise exceptions.ValidationError(msg)
		else:
			msg = 'Must include "email" and "password"'
			raise exceptions.ValidationError(msg)

		attrs['user'] = user

		return attrs
