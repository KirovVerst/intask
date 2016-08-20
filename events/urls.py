from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from events.views import *

router = DefaultRouter()
router.register(r'events', EventViewSet, base_name='events')
router.register(r'events/(?P<event_id>[0-9]+)/tasks', TaskViewSet, base_name='tasks')
router.register(r'events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks', SubtaskViewSet, base_name='subtasks')

urlpatterns = router.urls

urlpatterns += [
    url(r'^events/(?P<event_id>[0-9]+)/users/?$', EventUserListCreateAPIView.as_view()),
    url(r'^events/(?P<event_id>[0-9]+)/users/(?P<pk>[0-9]+)/?$', EventUserRetrieveDestroyAPIView.as_view()),
]

urlpatterns += [
    url(r'^events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users/?$', TaskUserListCreateAPIView.as_view()),
    url(r'^events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users/(?P<pk>[0-9]+)/?$',
        TaskUserRetrieveDestroyAPIView.as_view())
]
