from api_logging import models

from ipware.ip import get_ip
import re, sys

def log_request(request):
    request_log = models.RequestLogEntry.objects.create(
        method=request.method,
        path=request.path,
        body=request.body,
        size=sys.getsizeof(request.body)
    )

    r = re.compile(r'^(HTTP_.+|CONTENT_TYPE|CONTENT_LENGTH)$')
    headers = {}
    for header in request.META:
        if r.match(header):
            clean_key = header.replace('HTTP_', '').replace('_', '-')
            headers[clean_key] = request.META[header]

    for header in headers:
        models.RequestHeader.objects.create(
            request=request_log,
            key=header,
            value=headers[header]
        )

    for param in request.query_params:
        models.QueryParam.objects.create(
            request=request_log,
            key=param,
            value=request.query_params[param]
        )

    return request_log

def log_response(response):
    return models.ResponseLogEntry.objects.create(
        status=response.status_code,
        content=response.content,
        size=sys.getsizeof(response.content)
    )

def log_call(api, request, response, consumer, seconds):
    models.APILogEntry.objects.create(
        api=api,
        request=log_request(request),
        response=log_response(response),
        caller_ip=get_ip(request),
        consumer=consumer,
        latency=int(seconds*1000)
    )
