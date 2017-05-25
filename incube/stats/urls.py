from django.conf.urls import include, url

from stats.views import APIStatsView

urlpatterns = [
    url(r'^stats/apis/(?P<pk>[0-9]+)/$', APIStatsView.as_view())
]
