from intask_api.subtasks.models import Subtask
from intask_api.tasks.models import Task
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class SubtaskSerializer(ModelSerializer):
    task = PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Subtask
        fields = ('id', 'title', 'is_completed', 'task')
