# coding=utf-8
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions, permissions, response, status, serializers, validators
from .serializers import EventSerializer, TaskSerializer, SubtaskSerializer, UserInEventSerializer, UserInTaskSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from .permissions import *
from invitations.models import Invitation
from datetime import datetime
from .invitations import invite_user_to_event


# Create your views here.

class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsParticipant(), ]
        return [IsEventHeader(), ]


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsParticipant()]
        return [IsEventHeader()]

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['pk'])

        if self.request.user == event.event_header:
            return event.task_set.all()

        return event.task_set.filter(Q(users=self.request.user) | Q(is_public=True)).distinct()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'task_header' not in data:
            data['task_header'] = request.user.id
        data['event'] = kwargs['pk']
        serializer = TaskSerializer(data=data)
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


class UserInEventViewSet(ModelViewSet):
    class UserInEvent(object):
        def __init__(self, user, event):
            self.user = user
            self.event = event

    serializer_class = UserInEventSerializer

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
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        result = [self.UserInEvent(user=user, event=event) for user in self.get_queryset()]
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['event_id'])

        try:
            user = User.objects.get(email=request.data['email'])
            """
            User found in database
            """
            if user in event.users.all():
                return Response(data={'error': "User has already been added in the event."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif event.add_email_to_list(request.data['email']):
                pass
            else:
                return Response(data="Email has already been in list of invited users.", status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            """
            User not found in database.
            """
            if event.add_email_to_list(request.data['email']):
                if invite_user_to_event(request.user, request.data['email'], event):
                    pass
                else:
                    return Response(data="Email with the invitation was not sent.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data="Email has already been in list of invited users.", status=status.HTTP_200_OK)

        invitation_data = {
            'event': event,
            'sender': request.user,
            'datetime': datetime.now(),
            'text': request.data['text'] if 'text' in request.data else "",
            'recipient': request.data['email']
        }
        Invitation.objects.create(**invitation_data)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['pk'])
        event = get_object_or_404(Event, id=kwargs['event_id'])
        if user in event.users.all():
            serializer = self.serializer_class(self.UserInEvent(user, event))
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


class UserInTaskViewSet(ModelViewSet):
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
        if user in task.users.all():
            task.users.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_200_OK)
