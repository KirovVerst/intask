from rest_framework.routers import DefaultRouter
from intask_api.projects.views import *

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'projects/(?P<project_id>[0-9]+)/users', ProjectUserViewSet, basename='project-users')

urlpatterns = router.urls
