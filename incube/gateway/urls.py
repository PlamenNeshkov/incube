from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from gateway import views

urlpatterns = [
    url(r'^', views.GatewayView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
