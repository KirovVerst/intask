# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from commenttables.models import *
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.

class Event(models.Model):
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(null=True, blank=True)
	finish_time = models.DateTimeField(null=True, blank=True)
	event_header = models.ForeignKey(User, related_name='event_header', default=None)
	users = models.ManyToManyField(User)
	invited_users = models.TextField(default="")

	COMPLETED = "COMPLETED"
	DELAYED = "DELAYED"
	IN_PROGESS = "IN_PROGRESS"
	STATUS_CHOICES = (
		(COMPLETED, "Completed"),
		(DELAYED, "Delayed"),
		(IN_PROGESS, "In progress")
	)
	status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=IN_PROGESS)
	comments = GenericRelation(CommentsTable, related_query_name='event')

	def add_email_to_list(self, email):
		"""
		:param email:
		:return: False if email has already been in list of invited users
		 	else True
		"""
		if email in self.invited_users.split(","):
			return False
		else:
			if len(self.invited_users) > 0:
				self.invited_users += ("," + email)
			else:
				self.invited_users = email
			self.save()
			return True


class Task(models.Model):
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(null=True, blank=True)
	finish_time = models.DateTimeField(null=True, blank=True)
	task_header = models.ForeignKey(User, related_name='task_header')
	users = models.ManyToManyField(User)
	is_public = models.BooleanField(default=False)
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
	finish_time = models.DateTimeField(null=True, blank=True)
	is_completed = models.BooleanField(default=False)
	task = models.ForeignKey(Task)
