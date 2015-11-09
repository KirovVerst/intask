from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions
from serializers import EventSerializer, TaskSerializer
from models import Event, Task


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
			event = Event.objects.get(Q(id=self.kwargs['pk']),
									  (Q(users=self.request.user) | Q(event_header=self.request.user)))
			if self.request.user == event.users or event.event_header == self.request.user:
				tasks = Task.objects.filter(event=event)
				is_public = Q(is_public=True)
				is_user = Q(users=self.request.user)
				is_task_header = Q(task_header=self.request.user)

				return tasks.filter(is_public | is_user | is_task_header)
		except ObjectDoesNotExist:
			raise exceptions.NotFound(detail="Not found.")
