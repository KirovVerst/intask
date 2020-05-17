from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task
from intask_api.projects.models import Project


class MemberTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.tasks = self.project.task_set.all()
        self.task = self.tasks.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.task_member = self.task.users.exclude(id=self.task.header.id).first()
        self.client.login(username=self.task_member.username, password="password")

    def test_get_task_list(self):
        url_params = dict(project_id=self.project.id)
        r = self.client.get(self.base_url, url_params)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(set(map(lambda x: x['id'], r.json())), set(self.tasks.values_list('id', flat=True)))

    def test_get_task(self):
        r = self.client.get(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.task.id)

    def test_patch_task(self):
        data = dict(title="amazing title")
        r = self.client.patch(self.task_url, data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        r = self.client.delete(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
