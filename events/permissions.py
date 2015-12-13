from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Event, Task


class IsEventHeader(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # subtask
        if hasattr(obj, 'task'):
            return obj.task.event.event_header == request.user
        # task
        if hasattr(obj, 'event'):
            return obj.event.event_header == request.user
        # event
        if hasattr(obj, 'event_header'):
            return obj.event_header == request.user


class IsTaskHeader(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.task_header == request.user


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()


class CanUpdateTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.event.event_header or request.user == obj.task_header


class CanRetrieveTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_event_header = obj.event.event_header
        return request.user in obj.users.all() or obj.is_public or is_event_header


class CanRetrieveSubtask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_event_header = obj.task.event.event_header
        is_participant = request.user in obj.task.users.all()
        is_public = obj.task.is_public
        return is_event_header | is_participant | is_public


class CanCreateUpdateDeleteSubtask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_event_header = obj.task.event.event_header == request.user
        is_task_header = obj.task.task_header == request.user
        return is_event_header | is_task_header


class CanCompleteSubtask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_event_header = obj.task.event.event_header
        is_participant = request.user in obj.task.users.all()
        return is_event_header | is_participant


class CanRetrieveUserInEvent(permissions.BasePermission):
    def has_permission(self, request, view):
        event = get_object_or_404(Event, id=view.kwargs['event_id'])
        return request.user in event.users.all()


class CanDeleteUserInEvent(permissions.BasePermission):
    def has_permission(self, request, view):
        event = get_object_or_404(Event, id=view.kwargs['event_id'])
        user = get_object_or_404(User, id=view.kwargs['pk'])

        is_event_header = event.event_header == request.user
        is_current_user = request.user == user
        return is_event_header | is_current_user


class CanAddUserInEvent(permissions.BasePermission):
    def has_permission(self, request, view):
        event = get_object_or_404(Event, id=view.kwargs['event_id'])
        return request.user == event.event_header


class CanRetrieveUserInTask(permissions.BasePermission):
    def has_permission(self, request, view):
        event = get_object_or_404(Event, id=view.kwargs['event_id'])
        is_participant_in_event = request.user in event.users.all()
        is_event_header = request.user == event.event_header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        is_public_task = task.is_public
        is_participant_in_task = request.user in task.users.all()

        return is_participant_in_event and (is_public_task | is_event_header | is_participant_in_task)


class CanAddUserInTask(permissions.BasePermission):
    def has_permission(self, request, view):
        event = get_object_or_404(Event, id=view.kwargs['event_id'])
        is_event_header = request.user == event.event_header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        is_task_header = request.user == task.task_header

        return is_event_header | is_task_header


class CanDeleteUserInTask(permissions.BasePermission):
    def has_permission(self, request, view):
        event = get_object_or_404(Event, id=view.kwargs['event_id'])
        is_event_header = request.user == event.event_header

        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        is_task_header = request.user == task.task_header

        return is_event_header | is_task_header
