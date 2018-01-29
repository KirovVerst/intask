from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from tasks import serializers
from rest_framework.exceptions import PermissionDenied
from tasks.permissions import *


# Create your views here.

class TaskViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        if self.action == "list":
            project = get_object_or_404(Project, id=self.request.GET.get('project_id', -1))
        else:
            project = get_object_or_404(Task, id=self.kwargs['pk']).project

        if self.request.user in project.users.all():
            return Task.objects.filter(project=project)
        else:
            raise PermissionDenied(detail="You aren't a project member.")

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), CanRetrieveTask()]
        elif self.request.method == "POST":
            return [permissions.IsAuthenticated(), ]
        elif self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), CanDeleteTask()]
        else:
            return [permissions.IsAuthenticated(), CanUpdateTask()]

    def create(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        return super(TaskViewSet, self).create(request, *args, **kwargs)


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
        serializer = serializers.TaskUserViewSerializer(instance=self.get_queryset(), many=True, context=self.kwargs)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an project.
        ---
        request_serializer: serializers.TaskUserCreateSerializer
        """
        serializer = serializers.TaskUserCreateSerializer(data=request.data, context=self.kwargs)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a task user.
        ---
        response_serializer: serializers.TaskUserViewSerializer
        """
        user = self.get_object()
        serializer = serializers.TaskUserViewSerializer(instance=user, context=self.kwargs)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an task.
        """
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        user = self.get_object()
        task.delete_user(user=user)
        return Response(status=status.HTTP_204_NO_CONTENT)
