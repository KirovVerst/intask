from django.conf.urls import include, url
from views import UserListAPIView, UserDetailAPIView

urlpatterns = [
	url(r'^/(?P<pk>[0-9]+)/?$', UserDetailAPIView.as_view(), name="get, delete and update the user"),
	url(r'$', UserListAPIView.as_view(), name="get the list of users or create a new user")
]
