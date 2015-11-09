from django.conf.urls import include, url
from views import *

urlpatterns = [
	url(r'^$', EventListCreateAPIView.as_view(), name="get the list of events or create a new event"),
	url(r'^(?P<pk>[0-9]+)/?$', EventDetailAPIView.as_view(), name="get, delete and update the event"),
	url(r'^(?P<pk>[0-9]+)/tasks/$', TaskListCreateAPIView.as_view()),
]
