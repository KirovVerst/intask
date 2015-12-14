from django.conf.urls import include, url
from invitations.views import InvitationAPIViewSet

urlpatterns = [
    url(r'^/?$', InvitationAPIViewSet.as_view({'post': 'invite'})),
]
