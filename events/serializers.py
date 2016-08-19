from rest_framework import serializers
from .models import Event, Subtask, Task
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    event_header = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ('title', 'description', 'event_header', 'finish_time')

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        event.users.add(event.event_header)
        event.save()
        return event

    def to_representation(self, instance):
        data = super(EventSerializer, self).to_representation(instance)
        data['event_header'] = UserSerializer(instance.event_header).data
        return data


class TaskSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    task_header = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('title', 'description', 'task_header', 'finish_time', 'event', 'status')

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.users.add(task.task_header)
        task.save()
        return task

    def to_representation(self, instance):
        data = super(TaskSerializer, self).to_representation(instance)
        data['task_header'] = UserSerializer(instance.task_header).data
        return data


class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Subtask
        fields = ('id', 'title', 'is_completed', 'task')

    def create(self, validated_data):
        return Subtask.objects.create(**validated_data)


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class UserInTaskSerializer(serializers.Serializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ('task', 'user',)

    def to_representation(self, instance):
        data = {
            'id': instance.user.id,
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'is_task_header': instance.task.task_header == instance.user
        }
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        pass
