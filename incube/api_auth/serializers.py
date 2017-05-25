from rest_framework import serializers
from api_auth import models

class AuthMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthMethod
        fields = ('id', 'api', 'auth_type', 'priority', 'is_active')

class BasicAuthCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BasicAuthCredentials
        fields = ('id', 'consumer', 'api', 'username', 'password')

class KeyCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeyCredentials
        fields = ('id', 'consumer', 'api', 'key')
        extra_kwargs = {'key': {'write_only': True}}

class AcceptedKeyParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcceptedKeyParameter
        fields = ('id', 'api', 'name', 'param_type')
