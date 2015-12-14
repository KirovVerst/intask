from django.shortcuts import render, get_object_or_404
from rest_framework import generics, response, status, exceptions, viewsets, views
from invitations.serializers import InvitationSerializer
from invitations.models import Invitation
from events.models import Event


# Create your views here.

class InvitationAPIViewSet(viewsets.ViewSet):
    def invite(self, request):
        invitation = get_object_or_404(Invitation, id=request.data['id'])
        event = invitation.event
        if self.request.data['accept']:
            event.users.add(self.request.user)
        event.remove_email_from_list(self.request.user.email)
        invitation.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
