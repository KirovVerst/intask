from rest_framework import serializers
from events.models import Event, Subtask, Task
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
        fields = ('id', 'title', 'description', 'task_header', 'finish_time', 'event', 'status')

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.users.add(task.task_header)
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


class EventUserViewSerializer(serializers.ModelSerializer):
    is_event_header = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_event_header')

    def to_representation(self, instance):
        data = super(EventUserViewSerializer, self).to_representation(instance)
        data['is_event_header'] = self.context['event_header'] == instance
        return data


class EventUserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        attrs['user'] = get_object_or_404(User, email=attrs['email'])
        return attrs


class TaskUserCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, attrs):
        attrs['user'] = get_object_or_404(User, email=attrs['user'])
        return attrs


class TaskUserViewSerializer(serializers.ModelSerializer):
    is_task_header = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_task_header')

    def to_representation(self, instance):
        data = super(TaskUserViewSerializer, self).to_representation(instance)
        data['is_task_header'] = self.context['task_header'] == instance
        return data
