from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CustomUser(models.Model):
    user = models.ForeignKey(User)
    phone_number = models.CharField(max_length=30, default=None, null=True)
