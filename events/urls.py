from django.conf.urls import include, url
from views import *

url_event = [
	url(r'^/(?P<pk>[0-9]+)/?$', EventDetailAPIView.as_view(), name="get, delete and update the event"),
	url(r'^/(?P<event_id>[0-9]+)/users/?$', UserInEventViewSet.as_view({
		'get': 'list_or_add',
		'post': 'list_or_add'
	})),
	url(r'^/(?P<event_id>[0-9]+)/users/(?P<user_id>[0-9]+)/?$',
		UserInEventViewSet.as_view({
			'get': 'remove_or_detail',
			'delete': 'remove_or_detail'
		})),
	url(r'$', EventListCreateAPIView.as_view(), name="get the list of events or create a new event"),
]

url_task = [
	url(r'^/(?P<pk>[0-9]+)/tasks/$', TaskListCreateAPIView.as_view(),
		name="get the list of tasks or create a new task"),

	url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailAPIView.as_view(),
		name="get, delete and update the task"),

	url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users/$',
		UserInTaskViewSet.as_view({
			'get': 'list_or_add',
			'post': 'list_or_add'
		})),

	url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users/(?P<user_id>[0-9]+)/',
		UserInTaskViewSet.as_view({
			'get': 'remove_or_detail',
			'delete': 'remove_or_detail'
		}))
]

url_subtask = [
	url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks/$', SubtaskListCreateAPIView.as_view(),
		name="get the list of task's subtasks or create a new subtask"),
	url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks/(?P<pk>[0-9]+)/$',
		SubtaskDetailAPIView.as_view(), name="get, delete or update the subtask")
]

urlpatterns = url_event + url_task + url_subtask
