from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task
from projects.models import Project
from django.contrib.auth.models import User


class ProjectHeaderTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()
        self.task_members = self.task.users.exclude(id=self.task.header.id)
        self.client.login(username=self.project.header.username, password="password")
        # different user types
        self.task_member = self.task_members.first()
        self.project_member = self.project.users.exclude(id=self.task.users.all()).exclude(
            id=self.task.project.header.id).first()
        self.no_project_member = User.objects.exclude(id=self.project.users.all()).first()
        # users url
        self.users_base_url = self.task_url + 'users/'
        self.user_url = self.users_base_url + '{0}/'.format(self.task_member.id)

    def test_get_list_tasks(self):
        url_params = dict(project_id=self.project.id)
        r = self.client.get(self.base_url, data=url_params)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(set(self.tasks.values_list('id', flat=True)), set(map(lambda x: x['id'], r.json())))

    def test_add_new_task(self):
        data = dict(title="my new task", project=self.project.id)

        # project header is a task header
        data["header"] = self.project.header.id
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(id=r.json()['id']).count(), 1)

        # project member is a task header
        data["header"] = self.project_member.id
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(id=r.json()['id']).count(), 1)

        # no project member is a task header
        data["header"] = self.no_project_member.id
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_new_task_with_incorrect_data(self):
        data = dict(project=self.project.id, header=self.project.header)

        # without title
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        data['title'] = "my new task"
        # no existing user is a task header
        data["header"] = max(User.objects.values_list('id', flat=True)) + 1
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        # no existing project
        data['header'] = self.project.header.id
        data['project'] = max(Project.objects.values_list('id', flat=True)) + 1
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_task(self):
        r = self.client.get(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.task.id)

    def test_patch_task(self):
        data = dict(title="updated title")
        r = self.client.patch(self.task_url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(r.json()['title'], self.task.title)

    def test_delete_task(self):
        r = self.client.delete(self.task_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=self.task.id).count(), 0)

    """
    TaskUsers API
    """

    # TODO: consider cases with different types of user
    def test_get_task_users_list(self):
        r = self.client.get(self.users_base_url)
        user_pks = set(self.task.users.values_list('id', flat=True))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(user_pks, set(map(lambda x: x['id'], r.json())))

    def test_add_new_user_in_task(self):
        data = dict(user=self.project_member.id)
        r = self.client.post(self.users_base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_delete_user_from_task(self):
        r = self.client.delete(self.user_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
