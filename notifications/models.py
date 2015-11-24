from django.db import models
from django.contrib.auth.models import User
from events.models import Event


# Create your models here.


class NotificationBody(models.Model):
	types = (
		("INVITATION_IN_EVENT", "INVITATION_IN_EVENT"),
		("ACCEPT_INVITATION", "ACCEPT_INVITATION"),
		("DECLINE_INVITATION", "DECLINE_INVITATION")
	)
	event = models.ForeignKey(Event, default=None)
	type = models.CharField(choices=types, default=None, max_length=100)
	sender = models.ForeignKey(User)
	text = models.TextField(max_length=1000, default=None)
	datetime = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
	body = models.ForeignKey(NotificationBody)
	recipient = models.EmailField(blank=False)
