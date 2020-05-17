from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from intask_api.projects.models import Project
from django.contrib.auth.models import User


# TODO: test changing datetimes
class ProjectsTest(APITestCase):
    fixtures = ['users.json', 'projects.json']
    base_url = '/api/v1/projects/'

    def setUp(self):
        self.project = Project.objects.first()
        self.members = self.project.users.all()
        self.project_url = self.base_url + "{0}/".format(self.project.id)
        # header_client
        self.header = self.project.header
        self.header_client = APIClient()
        self.header_client.login(username=self.header.username, password="password")
        # member_client
        self.member = self.members.exclude(id=self.project.header.id).first()
        self.member_client = APIClient()
        self.member_client.login(username=self.member.username, password="password")
        # not member client
        self.no_member = User.objects.all().exclude(id__in=self.members.values_list('id', flat=True)).first()
        self.no_member_client = APIClient()
        self.no_member_client.login(username=self.no_member.username, password="password")

    def test_list_projects(self):
        r = self.client.get(self.base_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        projects = Project.objects.filter(users=self.member)
        r = self.member_client.get(self.base_url).json()
        project_pks = set(map(lambda x: x['id'], r))
        self.assertEqual(set(projects.values_list('id', flat=True)), project_pks)

    def test_get_project(self):
        # anonymous
        r = self.client.get(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # header
        r = self.header_client.get(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.project.id)

        # member
        r = self.member_client.get(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.project.id)
        # not member
        r = self.no_member_client.get(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_project(self):
        # anonymous
        data = dict(title="new title")
        r = self.client.patch(self.project_url, data=data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        # header
        r = self.header_client.patch(self.project_url, data=data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['title'], data['title'])

        # member
        r = self.member_client.patch(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # not member
        r = self.no_member_client.get(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_make_no_member_to_be_a_header(self):
        # header is trying to set no-member on header position
        data = dict(header=self.no_member.id)
        r = self.header_client.patch(self.project_url, data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        # anonymous
        r = self.client.delete(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        # member
        r = self.member_client.delete(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # not member
        r = self.no_member_client.get(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

        # header
        r = self.header_client.delete(self.project_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.filter(id=self.project.id).count(), 0)

    def test_add_new_project(self):
        # anonymous
        data = dict(title="My new project")
        r = self.client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # not anonymous
        r = self.member_client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
