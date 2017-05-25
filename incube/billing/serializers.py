from rest_framework import serializers

from core.fields import HyperlinkedChildField
from billing import models

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = ('id', 'stripe_id', 'api', 'calls_per_interval', 'amount',
                  'currency', 'interval', 'interval_count', 'name', 'overage_call_cost')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = ('id', 'stripe_id', 'plan', 'consumer', 'enable_overage',
                  'current_period_start', 'current_period_end')
