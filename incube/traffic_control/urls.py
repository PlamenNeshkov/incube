from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from traffic_control import views

router = DefaultRouter()
router.register(
    r'request-size-limits',
    views.RequestSizeLimitViewSet,
    base_name='request-size-limit'
)

rate_limit_router = DefaultRouter()
rate_limit_router.register(
    r'ip-address',
    views.IPAddressRateLimitViewSet,
    base_name='ip-address-rate-limit'
)
rate_limit_router.register(
    r'consumer',
    views.ConsumerRateLimitViewSet,
    base_name='consumer-rate-limit'
)

urlpatterns = [
    url(r'^rate-limits/', include(rate_limit_router.urls)),
    url(r'^', include(router.urls)),
]
