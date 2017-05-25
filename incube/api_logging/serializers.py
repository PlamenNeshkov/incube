from rest_framework import fields
from rest_framework import relations
from rest_framework import serializers
from api_logging import models
from core.fields import HyperlinkedChildField

from collections import OrderedDict

class HttpParamMixin():
    class Meta:
        fields = ('key', 'value')

    def flatten(serializer_data):
        data = OrderedDict()
        for param in sorted(serializer_data, key=lambda d: d['key']):
            data[param['key']] = param['value']
        return data

class RequestHeaderSerializer(serializers.ModelSerializer, HttpParamMixin):
    class Meta(HttpParamMixin.Meta):
        model = models.RequestHeader

class QueryParamSerializer(serializers.ModelSerializer, HttpParamMixin):
    class Meta(HttpParamMixin.Meta):
        model = models.QueryParam

class RequestLogEntrySerializer(serializers.ModelSerializer):
    headers = fields.SerializerMethodField()
    query_params = fields.SerializerMethodField()

    class Meta:
        model = models.RequestLogEntry
        fields = ('method', 'path', 'query_params', 'headers', 'body', 'size')

    def get_headers(self, obj):
        serializer = RequestHeaderSerializer(obj.headers, many=True)
        return RequestHeaderSerializer.flatten(serializer.data)

    def get_query_params(self, obj):
        serializer = QueryParamSerializer(obj.query_params, many=True)
        return QueryParamSerializer.flatten(serializer.data)

class ResponseLogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResponseLogEntry
        fields = ('status', 'content', 'size')

class APILogEntrySerializer(serializers.HyperlinkedModelSerializer):
    request = RequestLogEntrySerializer(read_only=True)
    response = ResponseLogEntrySerializer(read_only=True)

    url = HyperlinkedChildField(view_name='log-detail', parent='api')

    class Meta:
        model = models.APILogEntry
        fields = ('id', 'url', 'api', 'request', 'response', 'latency',
                  'caller_ip', 'consumer', 'created')
