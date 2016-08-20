from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser
from .serializers import EventSerializer, TaskSerializer, SubtaskSerializer, EventUserViewSerializer, \
    TaskUserViewSerializer, EventUserCreateSerializer, TaskUserCreateSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from .permissions import *
from invitations.models import Invitation
from events.models import Subtask
from datetime import datetime
from users.serializers import UserSerializer
from rest_framework.views import APIView


# Create your views here.
class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, ]

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsParticipant()]
        return [permissions.IsAuthenticated(), IsEventHeader()]

    def create(self, request, *args, **kwargs):
        """
        Create a new event.
        ---

        """
        request.data['event_header'] = request.user.id
        return super(EventViewSet, self).create(request, *args, **kwargs)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        return Task.objects.filter(event=event)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsParticipant(), permissions.IsAuthenticated()]
        return [IsEventHeader(), permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        request.data['event'] = kwargs['event_id']
        return super(TaskViewSet, self).create(request, *args, **kwargs)


class SubtaskViewSet(ModelViewSet):
    serializer_class = SubtaskSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveSubtask(), ]
        return [CanCreateUpdateDeleteSubtask()]

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return Subtask.objects.filter(task=task)

    def create(self, request, *args, **kwargs):
        request.data['task'] = kwargs['task_id']
        return super(SubtaskViewSet, self).create(request, *args, **kwargs)


def get_event(pk):
    try:
        return get_object_or_404(Event, id=pk)
    except ObjectDoesNotExist:
        raise exceptions.NotFound("Event %s not found." % pk)


def get_task(event_id, pk):
    e = get_event(event_id)
    try:
        return get_object_or_404(e.task_set.all(), id=pk)
    except ObjectDoesNotExist:
        raise exceptions.NotFound("Event %s not found." % pk)


class EventUserListCreateAPIView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [CanRetrieveEventUser()]
        return [CanAddEventUser()]

    def list(self, request, *args, **kwargs):
        """
        List of users from the event
        ---
        """
        e = get_event(kwargs['event_id'])
        serializer = EventUserViewSerializer(instance=e.users.all(), many=True,
                                             context={'event_header': e.event_header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        e = get_event(kwargs['event_id'])
        serializer = EventUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        try:
            e.add_user(user)
            return Response(data=dict(msg="User has been added."))
        except Exception as ex:
            return Response(data=dict(msg=ex.args[0]), status=status.HTTP_400_BAD_REQUEST)


class EventUserRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [CanRetrieveEventUser()]
        return [CanDeleteEventUser()]

    def get_event(self):
        return get_object_or_404(Event, id=self.kwargs['event_id'])

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        e = get_object_or_404(Event, id=self.kwargs['event_id'])
        return e.users.all()

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        e = self.get_event()
        serializer = EventUserViewSerializer(instance=user, context={'event_header': e.event_header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        e = self.get_event()
        user = self.get_object()
        try:
            e.delete_user(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=dict(msg=ex.args[0]))


class TaskUserListCreateAPIView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [CanRetrieveTask()]
        return [CanAddTaskUser()]

    def list(self, request, *args, **kwargs):
        t = get_task(event_id=kwargs['event_id'], pk=kwargs['task_id'])
        serializer = TaskUserViewSerializer(instance=t.users.all(), many=True,
                                            context={'task_header': t.task_header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        task = get_task(kwargs['event_id'], pk=kwargs['task_id'])
        serializer = TaskUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        try:
            task.add_user(user)
            return Response(data=dict(msg="User has been added."))
        except Exception as ex:
            return Response(data=dict(msg=ex.args[0]), status=status.HTTP_400_BAD_REQUEST)


class TaskUserRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [CanRetrieveTaskUser()]
        return [CanDeleteTaskUser()]

    def get_queryset(self):
        task = get_task(event_id=self.kwargs['event_id'], pk=self.kwargs['task_id'])
        return task.users.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Get the user from the task
        """
        user = self.get_object()
        task = get_task(event_id=kwargs['event_id'], pk=kwargs['task_id'])
        serializer = TaskUserViewSerializer(instance=user, context={'task_header': task.task_header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        task = get_task(event_id=kwargs['event_id'], pk=kwargs['task_id'])
        try:
            user = self.get_object()
            task.delete_user(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=dict(msg=ex.args[0]))
