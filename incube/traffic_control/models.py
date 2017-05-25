from django.db import models
from core.models import BaseModel, API, Consumer

class RateLimit(BaseModel):
    SECOND = 'seconds'
    MINUTE = 'minutes'
    HOUR = 'hours'
    DAY = 'days'
    MONTH = 'months'
    YEAR = 'years'
    TIME_UNITS = (
        (SECOND, SECOND),
        (MINUTE, MINUTE),
        (HOUR, HOUR),
        (DAY, DAY),
        (MONTH, MONTH),
        (YEAR, YEAR),
    )

    api = models.OneToOneField(API, on_delete=models.CASCADE)
    call_amount = models.PositiveIntegerField()

    time_amount = models.PositiveIntegerField()
    time_unit = models.CharField(max_length=8, choices=TIME_UNITS)

    class Meta:
        abstract = True

class IPAddressRateLimit(RateLimit):
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('api', 'ip_address')

class ConsumerRateLimit(RateLimit):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('api', 'consumer')

class RequestSizeLimit(BaseModel):
    api = models.OneToOneField(API, on_delete=models.CASCADE)
    max_kilobytes = models.PositiveIntegerField()
