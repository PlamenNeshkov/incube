from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsApiOwner
from traffic_control import models, serializers

class IPAddressRateLimitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IPAddressRateLimitSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.IPAddressRateLimit.objects\
            .filter(api__owner=self.request.user.id)

class ConsumerRateLimitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ConsumerRateLimitSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.ConsumerRateLimit.objects\
            .filter(api__owner=self.request.user.id)

class RequestSizeLimitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RequestSizeLimitSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.RequestSizeLimit.objects\
            .filter(api__owner=self.request.user.id)
