from django.conf import settings

from rest_framework import status, viewsets, views, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from core import permissions
from core.models import API, Consumer

from billing import models
from billing import serializers

import stripe

class PlanViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):

    serializer_class = serializers.PlanSerializer
    permission_classes = (IsAuthenticated,
                          permissions.IsStripeConnected,
                          permissions.IsApiOwner)

    def to_id(self, str):
        return str.lower().strip().replace(' ', '-')

    def plan_id(self, api, name):
        return '{}-{}'.format(self.to_id(api), self.to_id(name))

    def get_queryset(self):
        return models.Plan.objects.filter(api__owner=self.request.user.id)

    def perform_create(self, serializer):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = serializer.validated_data

        plan = stripe.Plan.create(
            stripe_account=data.get('api').owner.stripe_account.stripe_id,
            id=self.plan_id(data.get('api').name, data.get('name')),
            name=data.get('name'),
            interval=data.get('interval'),
            interval_count=data.get('interval_count'),
            currency=data.get('currency'),
            amount=data.get('amount'),
        )
        serializer.save(stripe_id=plan.id)

    def perform_destroy(self, instance):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        plan = stripe.Plan.retrieve(
            stripe_account=instance.api.owner.stripe_account.stripe_id,
            id=self.plan_id(instance.api.name, instance.name)
        )
        plan.delete()
        instance.delete()

class RetrieveSubscriptionView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (IsAuthenticated,
                          permissions.IsStripeConnected,
                          permissions.IsPlanOwner)

    def get_queryset(self):
        return models.Subscription.objects.filter(plan__api__owner=self.request.user.id)
