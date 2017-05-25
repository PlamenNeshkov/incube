from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from billing import views

router = DefaultRouter()
router.register(
    r'plans',
    views.PlanViewSet,
    base_name='plan'
)
router.register(
    r'subscriptions',
    views.RetrieveSubscriptionView,
    base_name='subscription'
)

urlpatterns = [
    url(r'^', include(router.urls)),
]
