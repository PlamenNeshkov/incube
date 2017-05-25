from datetime import datetime, timedelta
from ipware.ip import get_ip
from sys import getsizeof

from traffic_control import models
from api_logging.models import APILogEntry

def get_rate_limit_delta_params(rate_limit):
    return {rate_limit.time_unit: rate_limit.time_amount}

def get_call_range(rate_limit):
    now = datetime.now()
    delta = get_rate_limit_delta_params(rate_limit)
    return [now - timedelta(**delta), now]

def get_calls_made(rate_limit):
    call_range = get_call_range(rate_limit)
    return APILogEntry.objects.filter(created__range=call_range).count()

def is_rate_limit_exceeded(rate_limit):
    if rate_limit:
        calls_made = get_calls_made(rate_limit)
        return calls_made > (rate_limit.call_amount + 1)
    else:
        return False

def is_ip_rate_limit_exceeded(api, request):
    ip = get_ip(request)
    rate_limit = models.IPAddressRateLimit.objects\
        .filter(api=api, ip_address=ip).first()
    return is_rate_limit_exceeded(rate_limit)

def is_consumer_rate_limit_exceeded(api, consumer):
    rate_limit = models.ConsumerRateLimit.objects\
        .filter(api=api, consumer=consumer).first()
    return is_rate_limit_exceeded(rate_limit)

def is_request_size_exceeded(api, request):
    request_size_limit = models.RequestSizeLimit.objects\
        .filter(api=api).first()
    if request_size_limit:
        request_size_kb = (getsizeof(request.data) +
                           getsizeof(request.query_params)) / 1000 # bytes to kb
        return request_size_kb > (request_size_limit.max_kilobytes + 1)
    else:
        return False
