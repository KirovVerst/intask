from django.conf.urls import include, url
from .views import ObtainAuthToken

urlpatterns = [
	url(r'^/login/?$', ObtainAuthToken.as_view()),
]
