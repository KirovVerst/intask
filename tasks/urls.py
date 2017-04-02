from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, TaskUserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='tasks')
router.register(r'tasks/(?P<task_id>[0-9]+)/users', TaskUserViewSet, base_name='task-users')
urlpatterns = router.urls
