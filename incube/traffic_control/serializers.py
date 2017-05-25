from rest_framework import serializers
from traffic_control import models

class IPAddressRateLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IPAddressRateLimit
        fields = ('id', 'api', 'call_amount',
                  'time_amount', 'time_unit', 'ip_address')

class ConsumerRateLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConsumerRateLimit
        fields = ('id', 'api', 'call_amount',
                  'time_amount', 'time_unit', 'consumer')

class RequestSizeLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RequestSizeLimit
        fields = ('id', 'api', 'max_kilobytes')
