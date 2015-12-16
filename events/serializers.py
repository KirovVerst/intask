from rest_framework import serializers
from .models import Event, Subtask, Task
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from users.models import CustomUser


class EventSerializer(serializers.ModelSerializer):
    event_header = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ('title', 'description', 'event_header', 'finish_time', 'status')

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        event.users.add(event.event_header)
        event.save()
        return event

    def to_representation(self, instance):
        # tasks = TaskSerializer(Task.objects.filter(event=instance), many=True).data
        # users = [{'id': user.id, 'email': user.email} for user in instance.users.all()]
        invited_users = instance.invited_users.split(",")
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'event_header': {
                'id': instance.event_header.id,
                'email': instance.event_header.email,
                'first_name': instance.event_header.first_name,
                'last_name': instance.event_header.last_name
            },
            # 'tasks': tasks,
            # 'users': users,
            'status': instance.status,
            'invited_users': invited_users if invited_users[0] != "" else [],
            'finish_time': instance.finish_time
        }


class TaskSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Task
        fields = ('title', 'description', 'task_header', 'is_public', 'finish_time', 'event', 'status')

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.users.add(task.task_header)
        task.save()
        return task

    def to_representation(self, instance):
        users = [user.id for user in instance.users.all()]
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'is_public': instance.is_public,
            'event': instance.event.id,
            'task_header': {
                'id': instance.task_header.id,
                'email': instance.task_header.email,
                'first_name': instance.task_header.first_name,
                'last_name': instance.task_header.last_name
            },
            'users': users,
            'status': instance.status,
            'finish_time': instance.finish_time
        }


class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Subtask
        fields = ('id', 'title', 'is_completed', 'task')

    def create(self, validated_data):
        return Subtask.objects.create(**validated_data)


class UserInEventSerializer(serializers.Serializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ('event', 'user')

    def to_representation(self, instance):
        custom_user = CustomUser.objects.get(user=instance.user)
        data = {
            'id': instance.user.id,
            'email': instance.user.email,
            'phone_number': custom_user.phone_number,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'is_event_header': instance.event.event_header == instance.user
        }
        # header_tasks = instance.event.task_set.filter(task_header=instance.user)
        # data['header_tasks'] = [{'id': task.id, 'title': task.title} for task in header_tasks]

        # user_tasks = instance.event.task_set.filter(users=instance.user)
        # data['user_tasks'] = [{'id': task.id, 'title': task.title} for task in user_tasks]
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def to_internal_value(self, data):
        pass


class UserInTaskSerializer(serializers.Serializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ('task', 'user',)

    def to_representation(self, instance):
        custom_user = CustomUser.objects.get(user=instance.user)
        data = {
            'id': instance.user.id,
            'email': instance.user.email,
            'phone_number': custom_user.phone_number,
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
