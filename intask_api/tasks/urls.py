from rest_framework.routers import DefaultRouter
from intask_api.tasks.views import TaskViewSet, TaskUserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'tasks/(?P<task_id>[0-9]+)/users', TaskUserViewSet, basename='task-users')
urlpatterns = router.urls
