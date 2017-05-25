from django.db import models
from core.models import BaseModel, API, Consumer

class RequestLogEntry(BaseModel):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('HEAD', 'HEAD'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('OPTIONS', 'OPTIONS'),
    ]

    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    path = models.CharField(max_length=1024)
    body = models.TextField(blank=True)
    size = models.IntegerField()

class ResponseLogEntry(BaseModel):
    status = models.CharField(max_length=3)
    content = models.TextField()
    size = models.IntegerField()

class APILogEntry(BaseModel):
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    request = models.OneToOneField(RequestLogEntry)
    response = models.OneToOneField(ResponseLogEntry)
    caller_ip = models.GenericIPAddressField()
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, blank=True, null=True)
    latency = models.PositiveIntegerField() # milliseconds

class HttpParam(BaseModel):
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.key, self.value)

    class Meta:
        abstract = True

class QueryParam(HttpParam):
    request = models.ForeignKey(RequestLogEntry, related_name='query_params', on_delete=models.CASCADE)

class RequestHeader(HttpParam):
    request = models.ForeignKey(RequestLogEntry, related_name='headers', on_delete=models.CASCADE)

class ResponseHeader(HttpParam):
    response = models.ForeignKey(ResponseLogEntry, on_delete=models.CASCADE)
