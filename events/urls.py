from django.conf.urls import include, url
from views import *

urlpatterns = [
	url(r'^$', EventListCreateAPIView.as_view(), name="get the list of events or create a new event"),
	url(r'^(?P<pk>[0-9]+)/?$', EventDetailAPIView.as_view(), name="get, delete and update the event"),

	url(r'^(?P<pk>[0-9]+)/tasks/$', TaskListCreateAPIView.as_view(),
		name="get the list of tasks or create a new task"),
	url(r'^(?P<event_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailAPIView.as_view(),
		name="get, delete and update the task"),

	url(r'^(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks/$', SubtaskListCreateAPIView.as_view(),
		name="get the list of task's subtasks or create a new subtask"),
	url(r'^(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks/(?P<pk>[0-9]+)/$',
		SubtaskDetailAPIView.as_view(), name="get, delete or update the subtask"),
]
