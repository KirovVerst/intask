from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions
from serializers import EventSerializer, TaskSerializer, SubtaskSerializer
from models import Event, Task, Subtask


# Create your views here.

class EventListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = EventSerializer

	def get_queryset(self):
		return Event.objects.filter(users=self.request.user)


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = EventSerializer

	def get_queryset(self):
		return Event.objects.filter(Q(users=self.request.user) | Q(event_header=self.request.user))


class TaskListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = TaskSerializer

	def get_queryset(self):
		try:
			event = Event.objects.get(Q(id=self.kwargs['pk']), Q(users=self.request.user))
			if self.request.user == event.users or event.event_header == self.request.user:
				tasks = Task.objects.filter(event=event)
				is_public = Q(is_public=True)
				is_participant = Q(users=self.request.user)
				return tasks.filter(is_public | is_participant)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = TaskSerializer

	def get_queryset(self):
		try:
			event = Event.objects.get(Q(id=self.kwargs['event_id']), Q(users=self.request.user))
			if self.request.user == event.users or event.event_header == self.request.user:
				tasks = Task.objects.filter(event=event)
				is_public = Q(is_public=True)
				is_participant = Q(users=self.request.user)
				return tasks.filter(is_public | is_participant)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Event not found.")


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
