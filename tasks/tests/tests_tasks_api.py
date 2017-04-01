from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task
from projects.models import Project


class AnonymousTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()

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


class ProjectHeaderTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()
        self.client.login(username=self.project.header.username, password="password")

    def test_get_list_tasks(self):
        url_params = dict(project_id=self.project.id)
        r = self.client.get(self.base_url, data=url_params)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(set(self.tasks.values_list('id', flat=True)), set(map(lambda x: x['id'], r.json())))

    def test_add_new_task(self):
        data = dict(title="my new task", project=self.project.id, header=self.project.header.id)
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(id=r.json()['id']).count(), 1)


class ProjectMemberTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()
        self.member = self.project.users.all().exclude(id=self.project.header.id).exclude(id=self.task.id).first()
        self.client.login(username=self.member.username, password="password")

    def test_get_list_tasks(self):
        url_params = dict(project_id=self.project.id)
        r = self.client.get(self.base_url, data=url_params)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertSetEqual(set(self.tasks.values_list('id', flat=True)), set(map(lambda x: x['id'], r.json())))

    def test_add_new_task(self):
        data = dict(title="my new task", project=self.project.id, header=self.member.id)
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(id=r.json()['id']).count(), 1)


class MemberTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()


class HeaderTasksTest(APITestCase):
    fixtures = ['users.json', 'projects.json', 'tasks.json']
    base_url = "/api/v1/tasks/"

    def setUp(self):
        self.project = Project.objects.first()
        self.task = self.project.task_set.first()
        self.task_url = self.base_url + '{0}/'.format(self.task.id)
        self.tasks = self.project.task_set.all()
