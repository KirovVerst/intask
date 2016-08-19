# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    finish_time = models.DateField(null=True, blank=True)
    event_header = models.ForeignKey(User, related_name='event_header', default=None)
    users = models.ManyToManyField(User)


class Task(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    finish_time = models.DateField(null=True)
    task_header = models.ForeignKey(User, related_name='task_header')
    users = models.ManyToManyField(User)
    event = models.ForeignKey(Event)

    COMPLETED = "COMPLETED"
    DELAYED = "DELAYED"
    IN_PROGESS = "IN_PROGRESS"
    STATUS_CHOICES = (
        (COMPLETED, "Completed"),
        (DELAYED, "Delayed"),
        (IN_PROGESS, "In progress")
    )
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=IN_PROGESS)


class Subtask(models.Model):
    title = models.CharField(max_length=100, null=False)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task)
