from django.conf.urls import include, url
from notifications.views import NotificationCreateListAPIView

urlpatterns = [
    url(r'$', NotificationCreateListAPIView.as_view())
]
