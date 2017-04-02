from rest_framework import permissions


class CanRetrieveSubtask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_project_header = obj.task.project.header == request.user
        is_participant = request.user in obj.task.users.all()
        return is_project_header | is_participant


class CanCreateUpdateDeleteSubtask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_project_header = obj.task.project.header == request.user
        is_task_header = obj.task.header == request.user
        is_task_member = request.user in obj.task.users.all()
        return is_project_header | is_task_header | is_task_member


class CanCompleteSubtask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_project_header = obj.task.project.header == request.user
        is_participant = request.user in obj.task.users.all()
        return is_project_header | is_participant
