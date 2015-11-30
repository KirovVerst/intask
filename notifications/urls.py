from django.conf.urls import include, url
from views import NotificationCreateListAPIView

urlpatterns = [
	url(r'$', NotificationCreateListAPIView.as_view())
]
