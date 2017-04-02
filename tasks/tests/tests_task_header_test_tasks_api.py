from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task
from projects.models import Project


class HeaderTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()
