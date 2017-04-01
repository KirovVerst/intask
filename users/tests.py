from django.test import TestCase
# Create your tests here.

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User


class UserTests(APITestCase):
    fixtures = ['auth.json']
    base_url = "/api/v1/"

    def setUp(self):
        self.auth_client = APIClient()
        self.auth_client.login(username="bross0@netising.org", password="password")
        self.auth_user_id = User.objects.get(username="bross0@netising.org").id
        self.auth_user_url = self.base_url + 'users/{0}/'.format(self.auth_user_id)
        super(UserTests, self).setUp()

    def test_sign_up(self):
        user_data = dict(email="email@email.com", password="password")
        curr_number = len(User.objects.all())
        url = self.base_url + "users/"
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(curr_number + 1, len(User.objects.all()))

    def test_login(self):
        user_data = dict(username="kirov@gmail.com", password="password")
        url = self.base_url + "auth/login/"
        r = self.client.post(url, user_data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_patch(self):
        new_first_name = "MyNewFirstName"
        r = self.auth_client.patch(self.auth_user_url, data={'first_name': new_first_name})
        self.assertEqual(r.json()['first_name'], new_first_name)
        self.assertEqual(User.objects.get(id=self.auth_user_id).first_name, new_first_name)

    def test_get_user(self):
        r = self.auth_client.get(self.auth_user_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['id'], self.auth_user_id)

    def test_delete(self):
        r = self.auth_client.delete(self.auth_user_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(User.objects.filter(id=self.auth_user_id)), 0)
