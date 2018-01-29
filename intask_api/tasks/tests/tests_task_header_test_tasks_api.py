from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task
from projects.models import Project
from django.contrib.auth.models import User


class HeaderTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.tasks = self.project.task_set.all()

        self.task = self.tasks.first()
        self.client.login(username=self.task.header.username, password="password")
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.task_member = self.task.users.exclude(id=self.task.header.id).first()

        self.another_task = self.project.task_set.exclude(id=self.task.id).first()
        self.another_task_url = self.base_url + '{0}/'.format(self.another_task.id)

        self.no_task_member = self.project.users.exclude(id=self.project.header.id).exclude(id=self.task.id).first()

    def test_get_list_tasks(self):
        url_params = dict(project_id=self.project.id)
        r = self.client.get(self.base_url, data=url_params)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(set(self.tasks.values_list('id', flat=True)), set(map(lambda x: x['id'], r.json())))

    def test_add_new_task(self):
        data = dict(title="my new task", project=self.project.id, header=self.no_task_member.id)
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(id=r.json()['id']).count(), 1)

    def test_delete_task(self):
        r = self.client.delete(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_task(self):
        data = dict(title="new title")
        r = self.client.patch(self.task_url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(r.json()['title'], self.task.title)

    def test_patch_task_header(self):
        # no task member
        r = self.client.patch(self.task_url, data=dict(header=self.no_task_member.id))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['header']['id'], Task.objects.get(id=self.task.id).header.id)

        # no project member
        candidate = User.objects.exclude(id=self.project.users.all()).first()
        r = self.client.patch(self.task_url, data=dict(header=candidate.id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

