from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^api/v1/auth/', include('authentication.urls')),
    url(r'^api/v1/users/', include('users.urls')),
    url(r'^api/v1/', include('projects.urls')),
    url(r'^api/v1/', include('tasks.urls')),
    url(r'^api/v1/', include('subtasks.urls')),
    url(r'^api/v1/docs/', schema_view),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
