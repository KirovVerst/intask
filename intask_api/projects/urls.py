from rest_framework.routers import DefaultRouter
from projects.views import *

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'projects/(?P<project_id>[0-9]+)/users', ProjectUserViewSet, base_name='project-users')

urlpatterns = router.urls
