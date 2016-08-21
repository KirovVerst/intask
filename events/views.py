from rest_framework import exceptions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from events import serializers
from events.permissions import *
from events.models import Subtask


# Create your views here.
class EventViewSet(ModelViewSet):
    serializer_class = serializers.EventSerializer
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
    serializer_class = serializers.TaskSerializer

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
    serializer_class = serializers.SubtaskSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [CanRetrieveSubtask(), ]
        return [CanCreateUpdateDeleteSubtask()]

    @property
    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return Subtask.objects.filter(task=task)

    def create(self, request, *args, **kwargs):
        request.data['task'] = kwargs['task_id']
        return super(SubtaskViewSet, self).create(request, *args, **kwargs)


def get_event(pk):
    try:
        return Event.objects.get(id=pk)
    except Exception:
        raise exceptions.NotFound("Event %s not found." % pk)


def get_task(event_id, task_id):
    e = get_event(event_id)
    try:
        return get_object_or_404(e.task_set.all(), id=task_id)
    except Exception:
        raise exceptions.NotFound("Event %s not found." % task_id)


class EventUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.EventUserViewSerializer
        else:
            return serializers.EventUserCreateSerializer

    def get_permissions(self):
        if self.action == "create":
            return [CanAddEventUser()]
        elif self.action == "destroy":
            return [CanDeleteEventUser()]
        else:
            return [CanRetrieveEventUser()]

    def get_event(self):
        return get_event(self.kwargs['event_id'])

    def get_queryset(self):
        event = self.get_event()
        return event.users.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of event users.
        ---
        response_serializer: serializers.EventUserViewSerializer
        """
        e = self.get_event()
        serializer = serializers.EventUserViewSerializer(instance=e.users.all(), many=True,
                                                         context={'event_header': e.event_header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an event.
        ---
        request_serializer: serializers.EventUserCreateSerializer
        """
        e = self.get_event()
        serializer = serializers.EventUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        try:
            e.add_user(user)
            return Response(data=dict(msg="User has been added."))
        except Exception as ex:
            return Response(data=dict(msg=ex.args[0]), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Get an event user.
        ---
        response_serializer: serializers.EventUserViewSerializer
        """
        user = self.get_object()
        e = self.get_event()
        serializer = serializers.EventUserViewSerializer(instance=user, context={'event_header': e.event_header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an event.
        """
        e = self.get_event()
        user = self.get_object()
        try:
            e.delete_user(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=dict(msg=ex.args[0]))


class TaskUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    def get_permissions(self):
        if self.request.method == "GET":
            return [CanRetrieveTaskUser()]
        elif self.request.method == "POST":
            return [CanAddTaskUser()]
        else:
            return [CanDeleteTaskUser()]

    def get_queryset(self):
        task = get_task(event_id=self.kwargs['event_id'], task_id=self.kwargs['task_id'])
        return task.users.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of task users.
        ---
        response_serializer: serializers.TaskUserViewSerializer
        """
        t = get_task(event_id=kwargs['event_id'], task_id=kwargs['task_id'])
        serializer = serializers.TaskUserViewSerializer(instance=t.users.all(), many=True,
                                                        context={'task_header': t.task_header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an event.
        """
        task = get_task(kwargs['event_id'], task_id=kwargs['task_id'])
        serializer = serializers.TaskUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        try:
            task.add_user(user)
            return Response(data=dict(msg="User has been added."))
        except Exception as ex:
            return Response(data=dict(msg=ex.args[0]), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a task user.
        ---
        response_serializer: serializers.TaskUserViewSerializer
        """
        user = self.get_object()
        task = get_task(event_id=kwargs['event_id'], task_id=kwargs['task_id'])
        serializer = serializers.TaskUserViewSerializer(instance=user, context={'task_header': task.task_header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an task.
        """
        task = get_task(event_id=kwargs['event_id'], task_id=kwargs['task_id'])
        try:
            user = self.get_object()
            task.delete_user(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=dict(msg=ex.args[0]))
