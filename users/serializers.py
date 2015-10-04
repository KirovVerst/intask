from rest_framework import serializers, validators
from django.contrib.auth.models import User
from models import CustomUser


class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(validators=[validators.UniqueValidator(queryset=User.objects.all()),
											   serializers.EmailValidator],
								  required=True)
	username = serializers.CharField(validators=[validators.UniqueValidator(queryset=User.objects.all())],
									 required=True)
	first_name = serializers.CharField(max_length=50,
									   required=False)
	last_name = serializers.CharField(max_length=50,
									  required=False)
	password = serializers.CharField(min_length=8,
									 required=True)
	field = serializers.CharField(max_length=50)

	class Meta:
		model = User
		fields = ('email', 'username', 'first_name', 'last_name', 'field', 'password')
		write_only = ('password',)

	def create(self, validated_data):
		custom_user_data = {
			"field": validated_data.pop("field", None)
		}
		user = User.objects.create(**validated_data)
		user.set_password(validated_data.pop('password'))
		user.save()

		custom_user_data['user'] = user
		CustomUser.objects.create(**custom_user_data)
		return user

	def to_representation(self, instance):
		custom_user = CustomUser.objects.get(user=instance)
		return {
			'email': instance.email,
			'first_name': instance.first_name,
			'last_name': instance.last_name,
			'username': instance.username,
			'field': custom_user.field
		}

	def update(self, instance, validated_data):
		instance.first_name = validated_data.pop('first_name', instance.first_name)
		instance.last_name = validated_data.pop('last_name', instance.last_name)
		instance.save()
		custom_user = CustomUser.objects.get(user=instance)
		custom_user.field = validated_data.pop('field', custom_user.field)
		custom_user.save()
		return instance
