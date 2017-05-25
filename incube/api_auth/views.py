from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsApiOwner
from api_auth import models, serializers

class AuthMethodViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthMethodSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.AuthMethod.objects\
            .filter(api__owner=self.request.user.id)

class BasicAuthCredentialsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BasicAuthCredentialsSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.BasicAuthCredentials.objects\
            .filter(api__owner=self.request.user.id)

class KeyCredentialsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.KeyCredentialsSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.KeyCredentials.objects\
            .filter(api__owner=self.request.user.id)

class AcceptedKeyParameterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AcceptedKeyParameterSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.AcceptedKeyParameter.objects\
            .filter(api__owner=self.request.user.id)
