from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from projects.models import Project
from django.contrib.auth.models import User


# TODO: test changing datetimes
class ProjectsTest(APITestCase):
    fixtures = ['users.json', 'projects.json']

    def setUp(self):
        self.project = Project.objects.first()
        self.members = self.project.users.all()
        self.base_url = "/api/v1/projects/{0}/users/".format(self.project.id)

        # header_client
        self.header = self.project.header
        self.header_client = APIClient()
        self.header_client.login(username=self.header.username, password="password")
        # member_client
        self.member = self.members.exclude(id=self.project.header.id).first()
        self.member_client = APIClient()
        self.member_client.login(username=self.member.username, password="password")
        self.member_url = self.base_url + '{0}/'.format(self.member.id)
        # not member client
        self.no_member = User.objects.all().exclude(id__in=self.members.values_list('id', flat=True)).first()
        self.no_member_client = APIClient()
        self.no_member_client.login(username=self.no_member.username, password="password")

    def test_anonymous_list_users(self):
        # anonymous
        r = self.client.get(self.base_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_list_users(self):
        data = self.member_client.get(self.base_url).json()
        project_pks = set(map(lambda x: x['id'], data))
        self.assertEqual(set(self.members.values_list('id', flat=True)), project_pks)

    def test_not_member_list_users(self):
        # not member
        r = self.no_member_client.get(self.base_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_get_member(self):
        # anonymous gets member
        r = self.client.get(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        # header gets member
        r = self.header_client.get(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.member.id)

        # member gets member
        r = self.member_client.get(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.member.id)

        # member gets another member
        another_member = self.project.users.all().exclude(id=self.member.id).first()
        r = self.member_client.get(self.base_url + '{0}/'.format(another_member.id))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], another_member.id)

        # not member gets member
        r = self.no_member_client.get(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_new_member(self):
        # anonymous
        data = dict(email=self.no_member.email)
        r = self.client.post(self.base_url, data=data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # member
        r = self.member_client.post(self.base_url, data=data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # no member
        r = self.no_member_client.post(self.base_url, data=data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # header
        r = self.header_client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_add_current_member(self):
        data = dict(email=self.member.email)
        r = self.header_client.post(self.base_url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        member_pks = self.project.users.all().values_list('id', flat=True)
        self.assertSetEqual(set(self.members.values_list('id', flat=True)), set(member_pks))

    def test_delete_member(self):
        # anonymous
        r = self.client.delete(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # member
        another_member = self.project.users.all().exclude(id=self.member.id).first()
        r = self.member_client.delete(self.base_url + '{0}/'.format(another_member.id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # no member
        r = self.no_member_client.delete(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        # header
        r = self.header_client.delete(self.member_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_header(self):
        # header is deleting himself from project
        header_url = self.base_url + '{0}/'.format(self.header.id)
        r = self.header_client.delete(header_url)
        print(r.json())
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_no_member(self):
        no_member_url = self.base_url + '{0}/'.format(self.no_member.id)
        r = self.header_client.delete(no_member_url)
        print(r.json())
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
