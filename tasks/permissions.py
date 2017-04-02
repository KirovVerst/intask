from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from tasks.models import Task
from projects.models import Project


class CanDeleteTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.project.header or request.user == obj.header


class CanUpdateTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.project.header or request.user == obj.header


class CanRetrieveTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_project_header = obj.project.header == request.user
        return request.user in obj.users.all() or is_project_header


class CanRetrieveTaskUser(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_id'])
        is_participant_in_project = request.user in project.users.all()
        is_project_header = request.user == project.header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        is_participant_in_task = request.user in task.users.all()

        return is_participant_in_project and (is_project_header | is_participant_in_task)


class CanAddTaskUser(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_id'])
        is_project_header = request.user == project.header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        is_task_header = request.user == task.header

        return is_project_header | is_task_header


class CanDeleteTaskUser(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_id'])
        is_project_header = request.user == project.header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        is_task_header = request.user == task.header

        user = get_object_or_404(User, id=view.kwargs['pk'])
        is_this_user = request.user == user

        return is_project_header | is_task_header | is_this_user
