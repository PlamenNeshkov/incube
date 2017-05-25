from django.conf.urls import include, url

from rest_framework.authtoken import views

urlpatterns = [
    url(r'^get-token/', views.obtain_auth_token),
    url(r'^session-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
