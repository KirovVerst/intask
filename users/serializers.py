from rest_framework import serializers
from django.contrib.auth.models import User
from models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser

	def create(self, validated_data):
		user_data = {
			'email': validated_data.pop('email'),
			'username': validated_data.pop('username'),
			'first_name': validated_data.pop('first_name', None),
			'last_name': validated_data.pop('last_name', None)
		}
		user = User.objects.create(**user_data)
		user.set_password(validated_data.pop('password'))
		user.save()
		field = validated_data.pop('field', None)
		return CustomUser.objects.create(field=field, user=user)
