# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# TODO: добавить ссылку на таблицу комментариев, добавить поле status (active, done, delayed)
# TODO: добавить статус для Event, Task, Subtask (in_progress, completed, delayed)

class Event(models.Model):
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(null=True, blank=True)
	finish_time = models.DateTimeField(null=True, blank=True)
	event_header = models.ForeignKey(User, related_name='event_header', default=None)
	users = models.ManyToManyField(User)


class Task(models.Model):
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(null=True, blank=True)
	finish_time = models.DateTimeField(null=True, blank=True)
	task_header = models.ForeignKey(User, related_name='task_header')
	users = models.ManyToManyField(User)
	is_public = models.BooleanField(default=False)
	event = models.ForeignKey(Event)


class Subtask(models.Model):
	title = models.CharField(max_length=100, null=False)
	finish_time = models.DateTimeField(null=True, blank=True)
	is_completed = models.BooleanField(default=False)
	task = models.ForeignKey(Task)
