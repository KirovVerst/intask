from rest_framework import serializers
from models import Event, Subtask, Task
from django.contrib.auth.models import User
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

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.description = validated_data.get('description', instance.description)
		instance.event_header = validated_data.get('event_header', instance.event_header)
		instance.status = validated_data.get('status', instance.status)
		instance.save()
		return instance

	def to_representation(self, instance):
		tasks = [{'id': task.id, 'title': task.title} for task in Task.objects.filter(event=instance)]
		users = [{'id': user.id, 'email': user.email} for user in instance.users.all()]
		return {
			'id': instance.id,
			'title': instance.title,
			'description': instance.description,
			'event_header': {
				'id': instance.event_header.id,
				'email': instance.event_header.email,
			},
			'tasks': tasks,
			'users': users,
			'status': instance.status
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

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.description = validated_data.get('description', instance.description)
		instance.task_header = validated_data.get('task_header', instance.task_header)
		instance.status = validated_data.get('status', instance.status)
		instance.save()

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
			'users': users,
			'status': instance.status
		}


class SubtaskSerializer(serializers.ModelSerializer):
	task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

	class Meta:
		model = Subtask
		fields = ('id', 'title', 'is_completed', 'task')

	def create(self, validated_data):
		return Subtask.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.title = validated_data.pop('title', instance.title)
		instance.is_completed = validated_data.pop('is_completed', instance.is_completed)
		instance.save()
		return instance


class UserInEventSerializer(serializers.Serializer):
	@staticmethod
	def to_json(event, user):
		custom_user = CustomUser.objects.get(user=user)
		data = {
			'id': user.id,
			'email': user.email,
			'phone_number': custom_user.phone_number,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'is_event_header': event.event_header == user
		}

		header_tasks = event.task_set.filter(task_header=user)
		data['header_tasks'] = [{'id': task.id, 'title': task.title} for task in header_tasks]

		user_tasks = event.task_set.filter(users=user)
		data['user_tasks'] = [{'id': task.id, 'title': task.title} for task in user_tasks]
		return data


class UserInTaskSerializer(serializers.Serializer):
	@staticmethod
	def to_json(task, user):
		custom_user = CustomUser.objects.get(user=user)
		data = {
			'id': user.id,
			'email': user.email,
			'phone_number': custom_user.phone_number,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'is_task_header': task.task_header == user
		}
		return data
