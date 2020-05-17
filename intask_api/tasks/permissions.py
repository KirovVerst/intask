from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from intask_api.tasks.models import Task
from intask_api.projects.models import Project


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
        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        member_of_project = request.user in task.project.users.all()
        project_header = request.user == task.project.header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        member_of_task = request.user in task.users.all()

        return member_of_project and (project_header | member_of_task)


class CanAddTaskUser(permissions.BasePermission):
    def has_permission(self, request, view):
        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        task_header = request.user == task.header
        project_header = request.user == task.project.header
        return project_header | task_header


class CanDeleteTaskUser(permissions.BasePermission):
    def has_permission(self, request, view):
        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        project_header = request.user == task.project.header

        task_header = request.user == task.header

        user = get_object_or_404(User, id=view.kwargs['pk'])
        profile_owner = request.user == user

        return project_header | task_header | profile_owner
