from django.conf.urls import include, url

from webhooks.views import WebhookView

urlpatterns = [
    url(r'^webhook/$', WebhookView.as_view())
]
