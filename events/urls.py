from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from events.views import *

users_in_event = DefaultRouter()
users_in_event.register(r'^/(?P<event_id>[0-9]+)/users/', UserInEventViewSet, 'UserInEvent')

url_event = [
    url(r'^/(?P<pk>[0-9]+)/?$', EventDetailAPIView.as_view(), name="get, delete and update the event"),
    url(r'/?$', EventListCreateAPIView.as_view(), name="get the list of events or create a new event"),
]

url_users_in_event = [
    url('^/(?P<event_id>[0-9]+)/invited_users/?$', InvitedUserInTaskViewSet.as_view({'post': 'destroy'})),
    url(r'^/(?P<event_id>[0-9]+)/users/?$', UserInEventViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^/(?P<event_id>[0-9]+)/users/(?P<pk>[0-9]+)/?$',
        UserInEventViewSet.as_view({'delete': 'destroy', 'get': 'retrieve'})),
]

url_task = [
    url(r'^/(?P<pk>[0-9]+)/tasks/?$', TaskListCreateAPIView.as_view(),
        name="get the list of tasks or create a new task"),

    url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/?$', TaskDetailAPIView.as_view(),
        name="get, delete and update the task"),
]

url_users_in_task = [
    url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users/?$',
        UserInTaskViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users/(?P<pk>[0-9]+)/?$',
        UserInTaskViewSet.as_view({'delete': 'destroy', 'get': 'retrieve'})),
]

url_subtask = [
    url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks/$', SubtaskListCreateAPIView.as_view(),
        name="get the list of task's subtasks or create a new subtask"),
    url(r'^/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks/(?P<pk>[0-9]+)/$',
        SubtaskDetailAPIView.as_view(), name="get, delete or update the subtask")
]

urlpatterns = url_users_in_event + url_users_in_task + url_task + url_subtask + url_event
