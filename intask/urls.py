from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^api/v1/auth/?', include('authentication.urls')),
    url(r'^api/v1/users', include('users.urls')),
    url(r'^api/v1/', include('events.urls')),
    url(r'^/?$', TemplateView.as_view(template_name='index.html')),
]
