from rest_framework import serializers, validators, exceptions
from django.contrib.auth.models import User
from models import CustomUser
from rest_framework.authtoken.models import Token
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(validators=[validators.UniqueValidator(queryset=User.objects.all()),
											   serializers.EmailValidator],
								   required=True)

	first_name = serializers.CharField(max_length=50,
									   allow_blank=True,
									   required=False)
	last_name = serializers.CharField(max_length=50,
									  required=False)
	password = serializers.CharField(min_length=8,
									 required=True)

	phone_number = serializers.CharField(max_length=50,
										 required=False)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'phone_number', 'password')
		write_only = ('password',)

	def create(self, validated_data):
		validated_data['username'] = validated_data['email']
		custom_user_data = {
			'phone_number': validated_data.pop('phone_number', None)
		}

		user = User.objects.create(**validated_data)
		user.set_password(validated_data.pop('password'))
		user.save()

		Token.objects.create(user=user)

		custom_user_data['user'] = user
		CustomUser.objects.create(**custom_user_data)
		return user

	def to_representation(self, instance):
		custom_user = CustomUser.objects.get(user=instance)
		token = Token.objects.get(user=instance)
		return {
			'id': instance.id,
			'token': token.key,
			'email': instance.email,
			'first_name': instance.first_name,
			'last_name': instance.last_name,
			'phone_number': custom_user.phone_number,
		}

	def update(self, instance, validated_data):
		instance.first_name = validated_data.pop('first_name', instance.first_name)
		instance.last_name = validated_data.pop('last_name', instance.last_name)
		instance.save()
		custom_user = CustomUser.objects.get(user=instance)
		custom_user.phone_number = validated_data.pop('phone_number', custom_user.phone_number)
		custom_user.save()
		return instance
