from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    finish_time = models.DateField(null=True)
    header = models.ForeignKey(User, related_name='task_header')
    users = models.ManyToManyField(User)
    project = models.ForeignKey(Project)

    COMPLETED = 1
    DELAYED = -1
    IN_PROGRESS = 0
    STATUS_CHOICES = (
        (COMPLETED, "Completed"),
        (DELAYED, "Delayed"),
        (IN_PROGRESS, "In progress")
    )
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=IN_PROGRESS)

    def delete_user(self, user):
        if user in self.users.all():
            if self.header == user:
                self.header = self.project.header
                self.save()
            self.users.remove(user)
        else:
            raise ValueError("User {0} not found.".format(user.id))

    def add_user(self, user):
        if self.users.filter(id=user).count() == 0:
            if user in self.project.users.all():
                self.users.add(user)
            else:
                raise ValueError("The user must be in the project.")
        else:
            raise ValueError("This user had already been added.")
