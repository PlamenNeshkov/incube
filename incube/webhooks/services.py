from django.conf import settings

from core.models import Consumer
from billing.models import Subscription

from datetime import datetime
import stripe

class Invoice:
    @staticmethod
    def _update_subscription(stripe_account, subcription_id):
        sub = Subscription.objects.get(stripe_id=subscription_id)
        stripe_sub = stripe.Subscription.retrieve(
            stripe_account=stripe_account,
            id=sub_id
        )
        sub.current_period_start = datetime.fromtimestamp(
            stripe_sub.current_period_start
        )
        sub.current_period_end = datetime.fromtimestamp(
            stripe_sub.current_period_end
        )
        sub.save()

    @staticmethod
    def payment_succeeded(stripe_account, invoice):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        customer = stripe.Customer.retrieve(
            stripe_account=stripe_account,
            id=invoice.get('customer')
        )

        lines = invoice.get('lines').get('data')
        for line in lines:
            if line.get('type') == 'subscription':
                Invoice._update_subscription(
                    stripe_account=stripe_account,
                    id=line.get('id')
                )
