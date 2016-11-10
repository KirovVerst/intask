from rest_framework import serializers, validators
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validators.UniqueValidator(queryset=User.objects.all())],
                                   required=True)

    password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']

        user = User.objects.create(**validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.save()
        return instance
