from django.conf import settings
from django.shortcuts import render

from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from webhooks.services import Invoice
import stripe, importlib

class WebhookView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        event = request.data
        if not (event.get('type') and event.get('user_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        stripe_account = event.get('user_id')

        # Stripe webhooks in the test environment cannot be retrieved back
        # for verification because they contain dummy data
        if not settings.DEBUG:
            stripe.Event.retrieve(
                stripe_account=stripe_account,
                id=event.get('id')
            )

        webhook_info = event['type'].split('.')

        class_name = webhook_info[0].capitalize()
        method_name = webhook_info[1]
        webhook_module = importlib.import_module('webhooks.services')
        try:
            webhook_class = getattr(webhook_module, class_name)
            webhook_method = getattr(webhook_class, method_name)
        except (KeyError, AttributeError) as e:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        try:
            webhook_method(stripe_account, event.get('data').get('object'))
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
