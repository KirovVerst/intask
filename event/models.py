from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Event(models.Model):
	title = models.CharField(max_length=100, null=False)
