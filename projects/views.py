from rest_framework import exceptions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from projects import serializers
from projects.permissions import *


# Create your views here.
class ProjectViewSet(ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    parser_classes = [MultiPartParser, ]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsParticipant()]
        elif self.request.method == "PATCH":
            return [permissions.IsAuthenticated(), IsProjectHeader(), CanChangeProjectHeader()]
        return [permissions.IsAuthenticated(), IsProjectHeader()]

    def create(self, request, *args, **kwargs):
        """
        Create a new project.
        """
        request.data['header'] = request.user.id
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete the project by id
        """
        return super(ProjectViewSet, self).destroy(self, request, args, kwargs)


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
