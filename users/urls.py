from django.conf.urls import include, url

from views import CustomUserListAPIView

urlpatterns = [
    url(r'^/$', CustomUserListAPIView.as_view(), name="get the list of users or create a new user"),
]
