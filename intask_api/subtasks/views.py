from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from intask_api.tasks.models import Task

from intask_api.subtasks.serializers import SubtaskSerializer
from intask_api.subtasks.models import Subtask
from intask_api.subtasks import permissions


# Create your views here.

class SubtaskViewSet(ModelViewSet):
    serializer_class = SubtaskSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [permissions.CanRetrieveSubtask(), ]
        return [permissions.CanCreateUpdateDeleteSubtask()]

    def get_queryset(self):
        if self.action == "list":
            task = get_object_or_404(Task, id=self.request.GET.get('task_id', -1))
        else:
            task = get_object_or_404(Subtask, id=self.kwargs['pk']).task
        return Subtask.objects.filter(task=task)

    def create(self, request, *args, **kwargs):
        """
        Create a new subtask.
        """
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
