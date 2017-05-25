from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, CreateUserView

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    url(r'^users/$', CreateUserView.as_view()),
    url(r'^', include(router.urls)),
]
