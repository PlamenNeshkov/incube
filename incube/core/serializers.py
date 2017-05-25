from rest_framework import serializers
from core import models

from api_auth.serializers import AuthMethodSerializer

class APISerializer(serializers.HyperlinkedModelSerializer):
    logs = serializers.HyperlinkedIdentityField(view_name='api-logs')
    auth_methods = AuthMethodSerializer(many=True, read_only=True)
    owner = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name='user-detail')

    class Meta:
        model = models.API
        fields = ('url', 'id', 'name', 'owner', 'subdomain', 'proxy_protocol',
                  'proxy_host', 'logs', 'auth_methods')
        read_only_fields = ('owner',)

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Consumer
        fields = ('id', 'stripe_id', 'custom_id', 'owner', 'source')
        read_only_fields = ('stripe_id', 'owner')
        extra_kwargs = {'source': {'write_only': True}}
