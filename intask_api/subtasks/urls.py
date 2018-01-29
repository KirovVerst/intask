from rest_framework.routers import DefaultRouter
from subtasks.views import SubtaskViewSet

router = DefaultRouter()
router.register(r'subtasks', SubtaskViewSet, base_name='subtasks')

urlpatterns = router.urls
