from django.test import TestCase
from models import Notification
from serializers import NotificationSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class NotificationTests(APITestCase):
	def create_simple_notification(self):
		data = {
			'text': 'The first notification',
			'type': 'INVITATION_IN_EVENT',
			'sender': 4,
			'recipient': 'ufa1409@mail.com'
		}

		notification_serializer = NotificationSerializer(data=data)
		notification = notification_serializer.save()
		print notification
