from rest_framework import serializers, exceptions
from invitations.models import Invitation
from django.contrib.auth.models import User
from events.models import Event
from django.core.mail import send_mail


class InvitationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                required=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=True)

    recipient = serializers.EmailField(required=True)

    class Meta:
        model = Invitation
        fields = ('sender', 'event', 'recipient', 'text')

    def create(self, validated_data):
        return Invitation.objects.create(**validated_data)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'datetime': instance.datetime,
            'sender': {
                'id': instance.sender.id,
                'email': instance.sender.email,
                'first_name': instance.sender.first_name,
                'last_name': instance.sender.last_name
            },
            'text': instance.text,
            'event': {
                'id': instance.event.id,
                'title': instance.event.title
            },
            'recipient': {
                'email': instance.recipient
            }
        }
