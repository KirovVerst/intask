# coding=utf-8
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions, status
from rest_framework.parsers import MultiPartParser
from .serializers import EventSerializer, TaskSerializer, SubtaskSerializer, EventUserSerializer, UserInTaskSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from .permissions import *
from invitations.models import Invitation
from datetime import datetime
from users.serializers import UserSerializer


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
        request.data['event_header'] = request.user.id
        return super(EventViewSet, self).create(request, *args, **kwargs)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        q = Task.objects.filter(event=event)
        return q

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsParticipant(), permissions.IsAuthenticated()]
        return [IsEventHeader(), permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        request.data['event'] = kwargs['event_id']
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveTask()]
        elif self.request.method == "DELETE":
            return [IsEventHeader(), ]
        else:
            return [CanUpdateTask(), ]

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])

        if self.request.user == event.event_header:
            return event.task_set.all()

        return event.task_set.filter(Q(users=self.request.user) | Q(is_public=True)).distinct()


class SubtaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SubtaskSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveSubtask(), ]
        else:
            return [CanCreateUpdateDeleteSubtask()]

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return task.subtask_set.all()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['task'] = kwargs['task_id']
        serializer = SubtaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubtaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveSubtask(), ]
        else:
            return [CanCreateUpdateDeleteSubtask()]

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return task.subtask_set.all()


class EventUsersViewSet(ModelViewSet):
    class UserInEvent(object):
        def __init__(self, user, event):
            self.user = user
            self.event = event

    serializer_class = EventUserSerializer

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        return event.users.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveUserInEvent(), ]
        elif self.request.method == "DELETE":
            return [CanDeleteUserInEvent(), ]
        elif self.request.method == "POST":
            return [CanAddUserInEvent(), ]
        else:
            raise exceptions.MethodNotAllowed(method=self.request.method)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['pk'])
        event = get_object_or_404(Event, id=kwargs['event_id'])
        if user in event.users.all():
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound()

    def destroy(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['event_id'])
        user = get_object_or_404(User, id=kwargs['pk'])
        if user in event.users.all():
            event.users.remove(user)
            for task in event.task_set.all():
                task.users.remove(user)
                task.task_header = event.event_header
                task.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_200_OK)


class InvitedUserInTaskViewSet(ModelViewSet):
    permission_classes = [IsEventHeader, ]
    serializer_class = UserInTaskSerializer

    def destroy(self, request, *args, **kwargs):
        email = request.data['email']
        event = get_object_or_404(Event, id=kwargs['event_id'])
        invited_users = event.invited_users.split(',')
        if email in invited_users:
            event.remove_email_from_list(email)
            Invitation.objects.get(event=event, recipient=email).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_200_OK)


class TaskUsersViewSet(ModelViewSet):
    class UserInTask(object):
        def __init__(self, user, task):
            self.user = user
            self.task = task

    serializer_class = UserInTaskSerializer

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        task = get_object_or_404(event.task_set.all(), id=self.kwargs['task_id'])
        return task.users.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveUserInTask(), ]
        elif self.request.method == "DELETE":
            return [CanDeleteUserInTask(), ]
        elif self.request.method == "POST":
            return [CanAddUserInTask(), ]
        else:
            raise exceptions.MethodNotAllowed(method=self.request.method)

    def list(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['task_id'])
        result = [self.UserInTask(user=user, task=task) for user in self.get_queryset()]
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['event_id'])
        task = get_object_or_404(event.task_set.all(), id=kwargs['task_id'])
        user = get_object_or_404(event.users.all(), id=request.data['user'])
        if user in task.users.all():
            return Response(status=status.HTTP_200_OK)
        else:
            task.users.add(user)
            return Response(self.serializer_class(self.UserInTask(user=user, task=task)).data,
                            status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['pk'])
        task = get_object_or_404(Task, id=kwargs['task_id'])
        if user in task.users.all():
            serializer = self.serializer_class(self.UserInTask(user, task))
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound()

    def destroy(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['task_id'])
        user = get_object_or_404(User, id=kwargs['pk'])
        event = get_object_or_404(Event, id=kwargs['event_id']);
        if user == task.task_header:
            task.users.add(event.event_header)
            task.task_header = event.event_header
            task.save()
        if user in task.users.all():
            task.users.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_200_OK)
