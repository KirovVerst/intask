from django.db.models import Count

from rest_framework.test import APITestCase
from rest_framework import status
from projects.models import Project
from subtasks.models import Subtask


# Create your tests here.


class SubtasksAPITestCase(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json', 'subtasks.json']
    base_url = '/api/v1/subtasks/'

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.annotate(user_count=Count('users')).filter(user_count__gt=1).first()
        self.member_task = self.task.users.all().exclude(id=self.task.header.id).first()
        self.client.login(username=self.member_task.username, password="password")
        self.subtasks = self.task.subtask_set.all()
        self.subtask = self.task.subtask_set.first()
        self.subtask_url = self.base_url + '{0}/'.format(self.subtask.id)

    def test_get_list_of_subtasks(self):
        url_params = dict(task_id=self.task.id)
        r = self.client.get(self.base_url, url_params)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(set(map(lambda x: x['id'], r.json())), set(self.subtasks.values_list('id', flat=True)))

    def test_add_new_subtask(self):
        data = dict(title="subtask_name", task=self.task.id)
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subtask.objects.filter(id=r.json()['id']).count(), 1)

    def test_delete_subtask(self):
        r = self.client.delete(self.subtask_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_subtask(self):
        data = dict(title="new title")
        r = self.client.patch(self.subtask_url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], r.json()['title'])
        self.assertEqual(Subtask.objects.get(id=self.subtask.id).title, r.json()['title'])
