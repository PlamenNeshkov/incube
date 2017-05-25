from django.conf.urls import include, url

from api_logging.views import LogDetailView

urlpatterns = [
    url(
        r'^apis/(?P<api_pk>[0-9]+)/logs/(?P<pk>[0-9]+)/$',
        LogDetailView.as_view(), name='log-detail'
    ),
]
