from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api_auth import views

router = DefaultRouter()
router.register(
    r'auth-methods',
    views.AuthMethodViewSet,
    base_name='auth-method'
)
router.register(
    r'accepted-key-params',
    views.AcceptedKeyParameterViewSet,
    base_name='accepted-key-param'
)

credentials_router = DefaultRouter()
credentials_router.register(
    r'key',
    views.KeyCredentialsViewSet,
    base_name='key-credentials'
)
credentials_router.register(
    r'basic-auth',
    views.BasicAuthCredentialsViewSet,
    base_name='basic-auth-credentials'
)

urlpatterns = [
    url('^credentials/', include(credentials_router.urls)),
    url('^', include(router.urls)),
]
