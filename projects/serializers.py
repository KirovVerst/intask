from rest_framework import serializers
from projects.models import Project
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    header = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ('title', 'description', 'header', 'finish_time', 'id')

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        project.users.add(project.header)
        return project

    def to_representation(self, instance):
        data = super(ProjectSerializer, self).to_representation(instance)
        data['header'] = UserSerializer(instance.header).data
        return data


class ProjectUserViewSerializer(serializers.ModelSerializer):
    is_header = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_header')

    def to_representation(self, instance):
        data = super(ProjectUserViewSerializer, self).to_representation(instance)
        data['is_header'] = self.context['header'] == instance
        return data


class ProjectUserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        attrs['user'] = get_object_or_404(User, email=attrs['email'])
        return attrs
