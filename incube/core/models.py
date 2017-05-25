from django.conf import settings
from django.db import models
from core import managers

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class API(BaseModel):
    HTTP = 'http'
    HTTPS = 'https'
    PROTOCOL_CHOICES = [
        (HTTP, HTTP),
        (HTTPS, HTTPS),
    ]

    name = models.CharField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

    subdomain = models.CharField(max_length=64, unique=True)
    proxy_protocol = models.CharField(choices=PROTOCOL_CHOICES,
                                      default=HTTPS,
                                      max_length=10)
    proxy_host = models.CharField(max_length=255)

    objects = managers.APIManager()

    def __str__(self):
        return "{} API".format(self.name)

    class Meta:
        unique_together = ('name', 'owner')

class Consumer(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=128, null=True)
    custom_id = models.CharField(max_length=128, null=True)
    source = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.stripe_id
