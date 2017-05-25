from django.conf import settings
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core import models, permissions, serializers

from api_logging.models import APILogEntry
from api_logging.serializers import APILogEntrySerializer

from billing.models import Plan, Subscription
from billing.serializers import SubscriptionSerializer

from datetime import datetime
import stripe

class APIViewSet(ModelViewSet):
    serializer_class = serializers.APISerializer
    permission_classes = (IsAuthenticated, permissions.IsOwner)

    def get_queryset(self):
        return models.API.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route(methods=['get'])
    def logs(self, request, pk=None):
        api = self.get_object()
        log_entries = APILogEntry.objects.filter(api=api)
        page = self.paginate_queryset(log_entries)
        serializer = APILogEntrySerializer(page,
                                           many=True,
                                           context={'request': request})
        return self.get_paginated_response(serializer.data)

class ConsumerViewSet(ModelViewSet):
    serializer_class = serializers.ConsumerSerializer
    permission_classes = (IsAuthenticated,
                          permissions.IsStripeConnected,
                          permissions.IsOwner)

    def get_queryset(self):
        return models.Consumer.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = serializer.validated_data

        customer = stripe.Customer.create(
            stripe_account=self.request.user.stripe_account.stripe_id,
            email=data.get('email'),
            source=data.get('source')
        )

        serializer.save(
            owner=self.request.user,
            stripe_id=customer.id,
            source=getattr(customer, 'source', None)
        )

    def perform_destroy(self, instance):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = stripe.Customer.retrieve(
            stripe_account=instance.owner.stripe_account.stripe_id,
            id=instance.stripe_id
        )
        customer.delete()
        instance.delete()

    @detail_route(methods=['get'])
    def subscriptions(self, request, pk=None):
        consumer = self.get_object()
        subscriptions = Subscription.objects.filter(consumer=consumer)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(page,
                                            many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @detail_route(methods=['post'])
    def subscribe(self, request, pk=None):
        consumer = self.get_object()
        try:
            plan_id = request.data['plan_id']
        except KeyError:
            return Response({'detail': 'Plan_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        plan = Plan.objects.get(id=plan_id)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_subscription = stripe.Subscription.create(
            stripe_account=self.request.user.stripe_account.stripe_id,
            customer=consumer.stripe_id,
            plan=plan.stripe_id
        )

        current_period_start = datetime.fromtimestamp(
            stripe_subscription.current_period_start
        )
        current_period_end = datetime.fromtimestamp(
            stripe_subscription.current_period_end
        )
        subscription = Subscription.objects.create(
            stripe_id=stripe_subscription.id,
            plan=plan,
            consumer=consumer,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            enable_overage=request.data.get('enable_overage', False)
        )
        data = SubscriptionSerializer(subscription).data
        return Response(data, status=status.HTTP_201_CREATED)

    @detail_route(methods=['post'])
    def unsubscribe(self, request, pk=None):
        consumer = self.get_object()
        try:
            subscription_id = request.data['subscription_id']
        except KeyError:
            return Response({'detail': 'Subscription_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.get(id=subscription_id)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_subscription = stripe.Subscription.retrieve(
            id=subscription.stripe_id,
            stripe_account=subscription.consumer.owner.stripe_account.stripe_id,
        )
        stripe_subscription.delete()
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
