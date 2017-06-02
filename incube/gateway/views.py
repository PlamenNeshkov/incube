from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import API
from requests.exceptions import ConnectionError

from api_logging.services import log_call
from api_auth.models import AuthMethod
from api_auth.services import authenticate
from billing.services import authorize
from traffic_control.services import (
    is_ip_rate_limit_exceeded,
    is_consumer_rate_limit_exceeded,
    is_request_size_exceeded
)

from datetime import datetime
import requests
import re

class GatewayView(APIView):
    def extract(self, response):
        data = None
        try:
            data = response.json()
        except ValueError:
            data = response.text
        except AttributeError:
            data = response.content
        return Response(data)

    def consumer_proxy(self, api, request, method, consumer):
        if is_consumer_rate_limit_exceeded(api, consumer):
            return JsonResponse(
                {'message': 'Your rate limit has been exceeded'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        result = authorize(api, consumer)
        if not result['authorized']:
            return JsonResponse(
                {'message': result['message']},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return self.get_response(api, request, method)

    def auth_proxy(self, api, request, method, auth_methods):
        consumer = authenticate(api, request, auth_methods)
        if consumer:
            response = self.consumer_proxy(api, request, method, consumer)
        else:
            response = JsonResponse(
                {'message': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return {
            'response': response,
            'consumer': consumer
        }

    def get_response(self, api, request, method):
        proxy_url = "{protocol}://{host}{path}".format(
            protocol = api.proxy_protocol,
            host = api.proxy_host.rstrip('\/'),
            path = request.path)
        response = JsonResponse(
            {'message': 'Unable to connect to remote API host'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
        try:
            response = method(proxy_url)
        except ConnectionError:
            pass
        return response

    def proxy(self, request, method):
        try:
            api = API.objects.from_request(request)
        except API.DoesNotExist:
            return JsonResponse(
                {'message': 'API matching this request does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        if is_request_size_exceeded(api, request):
            return JsonResponse(
                {'message': 'Request is too large'},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

        if is_ip_rate_limit_exceeded(api, request):
            return JsonResponse(
                {'message': 'IP Address rate limit exceeded'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        auth_methods = AuthMethod.objects.filter(api=api, is_active=True)
        consumer = None

        start_time = datetime.now()

        if auth_methods:
            auth_proxy_result = self.auth_proxy(api, request, method, auth_methods)
            response = auth_proxy_result['response']
            consumer = auth_proxy_result['consumer']
        else:
            response = self.get_response(api, request, method)

        end_time = datetime.now()
        seconds = (end_time - start_time).total_seconds()
        log_call(api, request, response, consumer, seconds)

        return self.extract(response)

    def get(self, request, format=None):
        return self.proxy(request, requests.get)

    def post(self, request, format=None):
        return self.proxy(request, requests.posts)

    def put(self, request, format=None):
        return self.proxy(request, requests.put)

    def patch(self, request, format=None):
        return self.proxy(request, requests.patch)

    def delete(self, request, format=None):
        return self.proxy(request, requests.delete)

    def head(self, request, format=None):
        return self.proxy(request, requests.head)

    def options(self, request, format=None):
        return self.proxy(request, requests.options)

    def trace(self, request, format=None):
        return self.proxy(request, requests.trace)
