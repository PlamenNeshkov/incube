from datetime import datetime
from billing import models

from api_logging.models import APILogEntry

def authorize(api, consumer):
    subscription = models.Subscription.objects.filter(
        consumer=consumer,
        plan__api=api,
        current_period_end__gte=datetime.now()
    ).first()
    message = None
    authorized = True

    if not subscription:
        plans = models.Plan.objects.filter(api=api)
        if plans:
            authorized = False
            message = 'Customer does not have a valid subscription for this API'
        else:
            authorized = True
    else:
        current_period = [subscription.current_period_start, subscription.current_period_end]
        calls_made = APILogEntry.objects.filter(created__range=current_period).count()

        if calls_made > (subscription.plan.calls_per_interval + 1) and \
            not subscription.enable_overage:

            authorized = False
            message = 'Current subscription period calls exceeded'

    return {
        'authorized': authorized,
        'message': message
    }
