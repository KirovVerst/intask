from django.db import models
from django.contrib.auth.models import User
from events.models import Event


# Create your models here.


class Invitation(models.Model):
    event = models.ForeignKey(Event)
    sender = models.ForeignKey(User)
    text = models.TextField(max_length=1000, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    recipient = models.EmailField()
