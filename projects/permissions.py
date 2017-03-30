from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from projects.models import Project


class IsProjectHeader(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # subtask
        if hasattr(obj, 'task'):
            return obj.task.project.header == request.user
        # task
        if hasattr(obj, 'project'):
            return obj.project.header == request.user
        # project
        if hasattr(obj, 'header'):
            return obj.header == request.user


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()


class CanRetrieveProjectUser(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_id'])
        return request.user in project.users.all()


class CanDeleteProjectUser(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_id'])
        user = get_object_or_404(User, id=view.kwargs['pk'])

        is_project_header = project.header == request.user
        is_current_user = request.user == user
        return is_project_header | is_current_user


class CanAddProjectUser(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_id'])
        return request.user == project.header


