from django.db import models

from core import fields
from core.models import BaseModel, API, Consumer

class Plan(BaseModel):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'YEAR'
    INTERVALS = (
        (DAY, DAY),
        (WEEK, WEEK),
        (MONTH, MONTH),
        (YEAR, YEAR),
    )

    stripe_id = models.CharField(max_length=64, null=True)
    api = models.ForeignKey(API, on_delete=models.CASCADE)

    calls_per_interval = models.PositiveIntegerField()
    overage_call_cost = models.PositiveIntegerField()

    # Stripe fields
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=5, choices=INTERVALS)
    interval_count = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=64)

    def __str__(self):
        return "{} {} plan".format(self.api, self.name)

class Subscription(BaseModel):
    stripe_id = models.CharField(max_length=64, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    enable_overage = models.BooleanField(default=False)

    # Stripe fields
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()

    def __str__(self):
        return "{}'s subscription to {}".format(self.consumer, self.plan)

    class Meta:
        unique_together = ('plan', 'consumer')
