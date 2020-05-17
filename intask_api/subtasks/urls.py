from rest_framework.routers import DefaultRouter
from intask_api.subtasks.views import SubtaskViewSet

router = DefaultRouter()
router.register(r'subtasks', SubtaskViewSet, basename='subtasks')

urlpatterns = router.urls
