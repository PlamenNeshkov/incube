from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from core.views import APIViewSet, ConsumerViewSet

router = DefaultRouter()
router.register(r'apis', APIViewSet, base_name='api')
router.register(r'consumers', ConsumerViewSet, base_name='consumer')

urlpatterns = [
    url(r'^', include(router.urls))
]
