from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from projects.models import Project
from tasks.models import Task, Subtask
from users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    header = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'header', 'finish_time', 'project', 'status')

    def validate(self, attrs):
        if 'header' in attrs and 'project' in attrs:
            if attrs['header'] not in attrs['project'].users.all():
                raise exceptions.ValidationError(detail="Only project member can be a task header.")
        return attrs

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.users.add(task.header)
        return task

    def to_representation(self, instance):
        data = super(TaskSerializer, self).to_representation(instance)
        data['header'] = UserSerializer(instance.header).data
        return data


class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Subtask
        fields = ('id', 'title', 'is_completed', 'task')


class TaskUserCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, attrs):
        attrs['user'] = get_object_or_404(User, email=attrs['user'])
        return attrs


class TaskUserViewSerializer(serializers.ModelSerializer):
    is_header = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_header')

    def to_representation(self, instance):
        data = super(TaskUserViewSerializer, self).to_representation(instance)
        data['is_header'] = self.context['header'] == instance
        return data
