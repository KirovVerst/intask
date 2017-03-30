from django.test import TestCase
# Create your tests here.

from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    user_data = {
        'email': "email@email.com",
        'password': "password",
    }

    def test_login(self):
        url = "/api/v1/auth/login/"
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response.data
