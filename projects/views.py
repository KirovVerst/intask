from rest_framework import exceptions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from projects import serializers
from projects.permissions import *
from projects.models import Subtask


# Create your views here.
class ProjectViewSet(ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    parser_classes = [MultiPartParser, ]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsParticipant()]
        return [permissions.IsAuthenticated(), IsProjectHeader()]

    def create(self, request, *args, **kwargs):
        """
        Create a new project.
        """
        request.data['header'] = request.user.id
        return super(ProjectViewSet, self).create(request, *args, **kwargs)


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


def get_project(pk):
    try:
        return Project.objects.get(id=pk)
    except Exception:
        raise exceptions.NotFound("Project %s not found." % pk)


def get_task(project_id, task_id):
    e = get_project(project_id)
    try:
        return get_object_or_404(e.task_set.all(), id=task_id)
    except Exception:
        raise exceptions.NotFound("Project %s not found." % task_id)


class ProjectUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ProjectUserViewSerializer
        else:
            return serializers.ProjectUserCreateSerializer

    def get_permissions(self):
        if self.action == "create":
            return [CanAddProjectUser()]
        elif self.action == "destroy":
            return [CanDeleteProjectUser()]
        else:
            return [CanRetrieveProjectUser()]

    def get_project(self):
        return get_project(self.kwargs['project_id'])

    def get_queryset(self):
        project = self.get_project()
        return project.users.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of project users.
        ---
        response_serializer: serializers.ProjectUserViewSerializer
        """
        e = self.get_project()
        serializer = serializers.ProjectUserViewSerializer(instance=e.users.all(), many=True,
                                                           context={'header': e.header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an project.
        ---
        request_serializer: serializers.ProjectUserCreateSerializer
        """
        e = self.get_project()
        serializer = serializers.ProjectUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        try:
            e.add_user(user)
            return Response(data=dict(msg="User has been added."))
        except Exception as ex:
            return Response(data=dict(msg=ex.args[0]), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Get an project user.
        ---
        response_serializer: serializers.ProjectUserViewSerializer
        """
        user = self.get_object()
        e = self.get_project()
        serializer = serializers.ProjectUserViewSerializer(instance=user, context={'header': e.header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an project.
        """
        e = self.get_project()
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
        task = get_task(project_id=self.kwargs['project_id'], task_id=self.kwargs['task_id'])
        return task.users.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of task users.
        ---
        response_serializer: serializers.TaskUserViewSerializer
        """
        t = get_task(project_id=kwargs['project_id'], task_id=kwargs['task_id'])
        serializer = serializers.TaskUserViewSerializer(instance=t.users.all(), many=True,
                                                        context={'task_header': t.task_header})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an project.
        ---
        request_serializer: serializers.TaskUserCreateSerializer
        """
        task = get_task(kwargs['project_id'], task_id=kwargs['task_id'])
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
        task = get_task(project_id=kwargs['project_id'], task_id=kwargs['task_id'])
        serializer = serializers.TaskUserViewSerializer(instance=user, context={'task_header': task.task_header})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an task.
        """
        task = get_task(project_id=kwargs['project_id'], task_id=kwargs['task_id'])
        try:
            user = self.get_object()
            task.delete_user(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=dict(msg=ex.args[0]))
