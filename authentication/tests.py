from django.test import TestCase
# Create your tests here.

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class AuthTests(APITestCase):
	def test_create_account(self):
		email = "kirov.verst@gmail.com"
		password = "123456789"
		url = "/api/users/"
		data = {'email': email, 'password': password}

		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1)

		url = "/api/auth/login"
		data = {'email': email, 'password': password}
		response = self.client.post(url, data, format='json')
		print response
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def get_credentials(self, **data):
		url = "/api/users/"
		response_create = self.client.post(url, data, format='json')

		url = "/api/auth/login/"
		response = self.client.post(url, data, format='json')
		return {
			'id': response.data['id'],
			'token': response.data['token']
		}