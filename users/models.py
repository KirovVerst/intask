from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CustomUser(models.Model):
	user = models.ForeignKey(User)
	field = models.CharField(max_length=50, null=True)
