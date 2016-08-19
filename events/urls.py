from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from events.views import *

router = DefaultRouter()
router.register(r'events', EventViewSet, base_name='events')
router.register(r'events/(?P<event_id>[0-9]+)/users', EventUsersViewSet, base_name='event-users')
router.register(r'events/(?P<event_id>[0-9]+)/tasks', TaskViewSet, base_name='tasks')
router.register(r'events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks', SubtaskViewSet, base_name='subtasks')
router.register(r'events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users', TaskUsersViewSet, base_name='task-user')
urlpatterns = router.urls

"""
event_urls = [
    url(r'^events/?$', EventListCreateAPIView.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/?$', EventDetailAPIView.as_view()),
    url(r'^events/(?P<event_id>[0-9]+)/users/?$', EventUsersViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^events/(?P<event_id>[0-9]+)/users/(?P<pk>[0-9]+)/?$',
        EventUsersViewSet.as_view({'delete': 'destroy', 'get': 'retrieve'})),
]
"""

"""
task_urls = [
    url(r'^tasks/?$', TaskListCreateAPIView.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)/?$', TaskDetailAPIView.as_view()),

    url(r'^tasks/(?P<task_id>[0-9]+)/users/?$', TaskUsersViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^tasks/(?P<task_id>[0-9]+)/users/(?P<pk>[0-9]+)/?$',
        TaskUsersViewSet.as_view({'delete': 'destroy', 'get': 'retrieve'})),
]

subtask_urls = [
    url(r'^subtasks/?$', SubtaskListCreateAPIView.as_view(),
        name="get the list of task's subtasks or create a new subtask"),
    url(r'^subtasks/(?P<pk>[0-9]+)/$', SubtaskDetailAPIView.as_view(), name="get, delete or update the subtask")
]
"""
