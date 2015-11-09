from rest_framework import serializers
from models import Event, Subtask, Task
from django.contrib.auth.models import User


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

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.description = validated_data.get('description', instance.description)
		instance.save()
		return instance

	def to_representation(self, instance):
		tasks = [{'id': task.id, 'title': task.title} for task in Task.objects.filter(event=instance)]
		users = [{'id': user.id, 'username': user.username} for user in instance.users.all()]
		return {
			'id': instance.id,
			'title': instance.title,
			'description': instance.description,
			'event_header': {
				'id': instance.event_header.id,
				'username': instance.event_header.username,
			},
			'tasks': tasks,
			'users': users
		}


class TaskSerializer(serializers.ModelSerializer):
	event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

	class Meta:
		model = Task
		fields = ('title', 'description', 'task_header', 'is_public', 'finish_time', 'event')

	def create(self, validated_data):
		task = Task.objects.create(**validated_data)
		task.users.add(task.task_header)
		task.save()
		return task

	def to_representation(self, instance):
		users = [{'id': user.id, 'username': user.username} for user in instance.users.all()]
		return {
			'id': instance.id,
			'title': instance.title,
			'description': instance.description,
			'is_public': instance.is_public,
			'event': instance.event.id,
			'task_header': {
				'id': instance.task_header.id,
				'username': instance.task_header.username
			},
			'users': users
		}
