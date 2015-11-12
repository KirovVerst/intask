from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from authentication.tests import AuthTests
from rest_framework import status
from rest_framework.authtoken.models import Token
from models import Event, Task


# Create your tests here.


class EventTests(APITestCase):
	user_data = {
		'email': 'kirov.verst@gmail.com',
		'password': 'password'
	}

	def test_create_event(self):
		user = User.objects.create(**self.user_data)
		token = Token.objects.create(user=user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		url = "/api/events/"
		data = {
			"title": "The first event",
			"description": "The first event's description",
			"event_header": user.id
		}

		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TaskTests(APITestCase):
	user_data = {
		'email': 'kirov.verst@gmail.com',
		'password': 'password'
	}

	def test_create_task(self):
		user = User.objects.create(**self.user_data)
		token = Token.objects.create(user=user)
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		url = "/api/events/"
		data = {
			"title": "The first event",
			"description": "The first event's description",
			"event_header": user.id
		}
		response = self.client.post(url, data, format='json')

		event = Event.objects.filter(event_header=user)[0]

		url = '/api/events/' + event.id.__str__() + "/tasks/"

		data = {
			'title': "The first task in the first event",
			"description": "The task's description",
			"task_header": user.id,
			"event": event.id
		}
		response = self.client.post(url, data, format='json')
		print response.data
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
