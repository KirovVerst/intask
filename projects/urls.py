from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from projects.views import *

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'projects/(?P<project_id>[0-9]+)/users', ProjectUserViewSet, base_name='project-users')
router.register(r'projects/(?P<project_id>[0-9]+)/tasks', TaskViewSet, base_name='tasks')
router.register(r'projects/(?P<project_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/subtasks', SubtaskViewSet,
                base_name='subtasks')
router.register(r'projects/(?P<project_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/users', TaskUserViewSet,
                base_name='task-users')

urlpatterns = router.urls
