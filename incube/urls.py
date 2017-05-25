from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('authentication.urls')),
    url(r'^', include('api_logging.urls')),
    url(r'^', include('api_auth.urls')),
    url(r'^', include('billing.urls')),
    url(r'^', include('webhooks.urls')),
    url(r'^', include('traffic_control.urls')),
    url(r'^', include('stats.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
