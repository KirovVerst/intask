from django.test import TestCase
# Create your tests here.

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authentication import Token
import json


class UserTests(APITestCase):
	user_data = {
		'email': "kirov.verst@gmail.com",
		'password': "123456789",
	}

	def test_create(self):
		url = "/api/users/"
		response = self.client.post(url, self.user_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1)
		return response.data

	def test_login(self):
		url = "/api/auth/login"
		response = self.client.post(url, self.user_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		return response.data

	def test_delete(self):
		response_create = self.test_create()
		response_login = self.test_login()
		token = response_login['token']
		id = response_create['id']
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

		url = "/api/users/" + id.__str__() + "/"
		response = self.client.delete(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def get_credentials(self):
		response_create = self.test_create()
		response_login = self.test_login()
		return {
			'token': response_login['token'],
			'id': response_create['id']
		}

	def test_update(self):
		credentials = self.get_credentials()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + credentials['token'])

		url = "/api/users/" + credentials['id'].__str__() + "/"
		data = {
			"first_name": "Kirov"
		}
		response = self.client.patch(url, data=data, format='json')
		self.assertEqual(json.loads(response.content)['first_name'], "Kirov")

		data = {
			"first_name": "Verst"
		}
		response = self.client.patch(url, data=data, format='json')
		self.assertEqual(json.loads(response.content)['first_name'], "Verst")

	def test_list(self):
		credentials = self.get_credentials()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + credentials['token'])
		url = "/api/users/"

		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
