from rest_framework import exceptions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from intask_api.projects.serializers import ProjectSerializer, ProjectUserCreateSerializer, ProjectUserViewSerializer
from intask_api.projects.permissions import *


# Create your views here.
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    parser_classes = [MultiPartParser, ]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated(), IsParticipant()]
        elif self.request.method == "PATCH":
            return [permissions.IsAuthenticated(), CanUpdateProject()]
        elif self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), CanDeleteProject()]
        elif self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        else:
            raise exceptions.MethodNotAllowed(method=self.request.method)

    def create(self, request, *args, **kwargs):
        """
        Create a new project.
        """
        request.data['header'] = request.user.id
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a project
        """
        return super(ProjectViewSet, self).destroy(self, request, args, kwargs)


class ProjectUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProjectUserViewSerializer
        else:
            return ProjectUserCreateSerializer

    def get_permissions(self):
        if self.action == "create":
            return [CanAddProjectUser()]
        elif self.action == "destroy":
            return [CanDeleteProjectUser()]
        else:
            return [CanRetrieveProjectUser()]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return project.users.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of project users.
        ---
        response_serializer: serializers.ProjectUserViewSerializer
        """
        serializer = ProjectUserViewSerializer(instance=self.get_queryset(), many=True, context=self.kwargs)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an user in an project.
        ---
        request_serializer: serializers.ProjectUserCreateSerializer
        """
        serializer = ProjectUserCreateSerializer(data=request.data, context=self.kwargs)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']
        return Response(data=user, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Get an project user.
        ---
        response_serializer: serializers.ProjectUserViewSerializer
        """
        user = self.get_object()
        serializer = ProjectUserViewSerializer(instance=user, context=self.kwargs)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an user from an project.
        """
        project = Project.objects.get(id=self.kwargs['project_id'])
        user = self.get_object()
        project.delete_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
