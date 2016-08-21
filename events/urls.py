from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from events.views import *

router = DefaultRouter()
router.register(r'events', EventViewSet, base_name='events')
router.register(r'events/(?P<event_id>[0-9]+)/users', EventUserViewSet, base_name='event-users')
router.register(r'events/(?P<event_id>[0-9]+)/tasks', TaskViewSet, base_name='tasks')
router.register(r'events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks', SubtaskViewSet, base_name='subtasks')
router.register(r'events/(?P<event_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users', TaskUserViewSet, base_name='task-users')

urlpatterns = router.urls
