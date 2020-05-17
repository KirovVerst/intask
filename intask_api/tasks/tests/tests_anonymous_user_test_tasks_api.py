from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from intask_api.projects.models import Project


class AnonymousTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()
        # users
        self.users_base_url = self.task_url + 'users/'
        self.user_url = self.users_base_url + '{0}/'.format(self.task.users.first().id)

    def test_tasks_list(self):
        url_params = dict(project_id=self.project.id)
        r = self.client.get(self.base_url, data=url_params)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task(self):
        r = self.client.get(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_new_task(self):
        data = dict(title="my new task", project=self.project.id, header=self.project.header.id)
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_task(self):
        data = dict(title="my updated task")
        r = self.client.patch(self.task_url, data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        r = self.client.delete(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    """
    TaskUsersAPI
    """

    def test_get_list_of_users_in_task(self):
        # GET : /api/v1/tasks/1/users/
        r = self.client.get(self.users_base_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_the_user_in_the_task(self):
        # GET : /api/v1/tasks/1/users/3/
        r = self.client.get(self.user_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_a_new_user_in_the_task(self):
        # POST: /api/v1/tasks/1/users/
        new_user = self.project.users.exclude(id=self.task.users.all()).first()
        r = self.client.post(self.users_base_url, data=dict(id=new_user.id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
