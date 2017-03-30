from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from tasks import serializers
from tasks.models import Subtask
from projects.permissions import IsProjectHeader
from tasks.permissions import *


# Create your views here.

class TaskViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return Task.objects.filter(project=project)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsParticipant(), permissions.IsAuthenticated()]
        return [IsProjectHeader(), permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        request.data['project'] = kwargs['project_id']
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
        """
        Create a new subtask.
        """
        request.data['task'] = kwargs['task_id']
        return super(SubtaskViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Get a list of subtasks.
        """
        return super(SubtaskViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a subtask.
        """
        return super(SubtaskViewSet, self).retrieve(request, *args, **kwargs)


class TaskUserViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    def get_permissions(self):
        if self.request.method == "GET":
            return [CanRetrieveTaskUser()]
        elif self.request.method == "POST":
            return [CanAddTaskUser()]
        else:
            return [CanDeleteTaskUser()]

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        return task.users.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of task users.
        ---
        response_serializer: serializers.TaskUserViewSerializer
        """
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer = serializers.TaskUserViewSerializer(instance=task.users.all(), many=True,
                                                        context={'task_header': task.task_header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an project.
        ---
        request_serializer: serializers.TaskUserCreateSerializer
        """
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
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
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer = serializers.TaskUserViewSerializer(instance=user, context={'task_header': task.task_header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an task.
        """
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        try:
            user = self.get_object()
            task.delete_user(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=dict(msg=ex.args[0]))
