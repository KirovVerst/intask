from rest_framework import serializers, exceptions
from .models import Notification, NotificationBody
from django.contrib.auth.models import User
from events.models import Event
from django.core.mail import send_mail


class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(source='notificationbody.sender', queryset=User.objects.all(),
                                                required=True)
    event = serializers.PrimaryKeyRelatedField(source='notificationbody.event', queryset=Event.objects.all(),
                                               required=True)
    text = serializers.CharField(source='notificationbody.text')
    type = serializers.ChoiceField(source='notificationbody.type', choices=NotificationBody().types)

    recipient = serializers.EmailField(required=True)

    class Meta:
        model = Notification
        fields = ('text', 'type', 'sender', 'event', 'recipient')

    def create(self, validated_data):
        body_data = validated_data.pop('notificationbody')
        body = NotificationBody.objects.create(**body_data)
        return Notification.objects.create(body=body, recipient=validated_data.pop('recipient'))

    def to_representation(self, instance):
        body = instance.body

        return {
            'id': instance.id,
            'type': body.type,
            'sender': {
                'id': body.sender.id,
                'email': body.sender.email,
                'first_name': body.sender.first_name,
                'last_name': body.sender.last_name
            },
            'text': body.text,
            'event': {
                'id': body.event.id,
                'title': body.event.title
            },
            'recipient': {
                'email': instance.recipient
            }
        }
