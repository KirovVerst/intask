from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    finish_time = models.DateField(null=True, blank=True)
    header = models.ForeignKey(User, related_name='project_header', default=None)
    users = models.ManyToManyField(User)

    def delete_user(self, user):
        if user in self.users.all():
            if self.header == user:
                raise ValueError("You can not delete the header before setting the other.")
            self.users.remove(user)
            for task in self.task_set.filter(users=user):
                task.delete_user(user=user)

    def add_user(self, user):
        self.users.add(user)
