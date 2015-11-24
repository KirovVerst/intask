from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions, permissions, response
from serializers import EventSerializer, TaskSerializer, SubtaskSerializer, UserInEventSerializer, UserInTaskSerializer
from models import Event, Task, Subtask
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


# Create your views here.

class EventListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = EventSerializer

	def get_queryset(self):
		return Event.objects.filter(users=self.request.user)


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = EventSerializer
	queryset = Event.objects.all()

	def get_queryset(self):
		return Event.objects.filter(users=self.request.user)


class TaskListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = TaskSerializer

	def get_queryset(self):
		try:
			event = Event.objects.get(id=self.kwargs['pk'])
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")

		if self.request.user not in event.users.all():
			raise exceptions.PermissionDenied(detail="You have not permission.")

		if self.request.user == event.event_header:
			return event.task_set.all()
		result = []
		for task in event.task_set.all():
			if self.request.user in task.users.all() or task.is_public:
				result.append(task)

		return result


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = TaskSerializer

	def get_queryset(self):
		try:
			event = Event.objects.get(id=self.kwargs['event_id'])
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")

		if self.request.user not in event.users.all():
			raise exceptions.PermissionDenied(detail="You have not permission.")

		if self.request.user == event.event_header:
			return event.task_set.all()
		result = []
		for task in event.task_set.all():
			if self.request.user in task.users.all() or task.is_public:
				result.append(task)

		return result


class SubtaskListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = SubtaskSerializer

	def get_queryset(self):
		try:
			event = Event.objects.get(Q(id=self.kwargs['event_id']), Q(users=self.request.user))
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")

		try:
			task = Task.objects.get(Q(id=self.kwargs['task_id']), Q(users=self.request.user))
			subtasks = Subtask.objects.filter(task=task)
			return subtasks
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Task not found.")


class SubtaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = SubtaskSerializer

	def get_queryset(self):
		try:
			event = Event.objects.get(Q(id=self.kwargs['event_id']), Q(users=self.request.user))
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")

		try:
			task = Task.objects.get(Q(id=self.kwargs['task_id']), Q(users=self.request.user))
			subtasks = Subtask.objects.filter(task=task)
			return subtasks
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Task not found.")


class UserInEventViewSet(ViewSet):
	def list_or_add(self, request, event_id):
		try:
			event = Event.objects.get(id=event_id, users=request.user)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")

		if request.method == "GET":
			users = event.users.all()
			result = [UserInEventSerializer.to_json(user=user, event=event) for user in users]
			return Response(result, status=200)
		else:
			user_id = request.data['user']

			try:
				user = User.objects.get(id=user_id)
			except ObjectDoesNotExist:
				raise exceptions.NotFound(detail="User not found.")

			event.users.add(user)

			data = {
				'text': 'The first notification',
				'type': 'INVITATION_IN_EVENT',
				'sender': self.request.user.id,
				'recipient': user.email,
				'event': event.id
			}

		notification_serializer = NotificationSerializer(data=data)
		notification_serializer.is_valid(raise_exception=True)
		notification = notification_serializer.save()

		return Response(data={'detail': 'User was added.'})


def remove_or_detail(self, request, event_id, user_id):
	try:
		event = Event.objects.get(id=event_id)
	except ObjectDoesNotExist:
		raise exceptions.NotFound(detail="Event not found.")
	try:
		user = User.objects.get(id=user_id)
	except ObjectDoesNotExist:
		raise exceptions.NotFound(detail="User not found.")

	if request.method == "GET":
		return Response(UserInEventSerializer.to_json(event=event, user=user))
	else:
		if event.event_header == user:
			return Response(
				{'message': 'User is the current event\'s owner. Change event_header before removal this user.'},
				status=400)
		event.users.remove(user)
		return Response({'message': 'User was deleted.'})


class UserInTaskViewSet(ViewSet):
	def list_or_add(self, request, event_id, task_id):
		try:
			event = Event.objects.get(id=event_id, users=request.user)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")
		try:
			task = event.task_set.get(id=task_id)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Task not found.")

		if request.method == "GET":
			users = task.users.all()
			result = [UserInTaskSerializer.to_json(task=task, user=user) for user in users]
			return Response(result, status=200)
		else:
			try:
				user = event.users.get(id=request.data['user_id'])
			except ObjectDoesNotExist:
				raise exceptions.NotFound(detail="User not found.")
			task.users.add(user)
			return Response({'detail': 'User was added.'})

	def remove_or_detail(self, request, event_id, task_id, user_id):
		try:
			event = Event.objects.get(id=event_id)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")

		try:
			task = event.task_set.get(id=task_id)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Task not found.")

		try:
			user = event.users.get(id=user_id)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="User not found.")

		if request.method == "GET":
			return Response(UserInTaskSerializer.to_json(task=task, user=user))
		else:
			if task.task_header == user:
				task.users.add(event.event_header)
				task.task_header = event.event_header

			task.users.remove(user)
			return Response({'detail': 'User was deleted.'})
