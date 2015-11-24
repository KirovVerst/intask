from rest_framework import serializers
from models import Notification, NotificationBody
from django.contrib.auth.models import User
from events.models import Event


class NotificationSerializer(serializers.ModelSerializer):
	recipient = serializers.EmailField(required=True)
	text = serializers.CharField(max_length=1000, required=False)
	type = serializers.ChoiceField(choices=NotificationBody.types, required=False)
	sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
	event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

	class Meta:
		model = Notification
		fields = ('recipient', 'text', 'type', 'sender', 'event')

	def create(self, validated_data):
		recipient = validated_data.pop('recipient')
		body = NotificationBody.objects.create(**validated_data)
		return Notification.objects.create(body=body, recipient=recipient)
