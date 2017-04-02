from django.db import models
from tasks.models import Task


# Create your models here.

class Subtask(models.Model):
    title = models.CharField(max_length=100, null=False)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task)
