from django.db import models, IntegrityError

from core.models import BaseModel, API, Consumer
from billing.models import Plan, Subscription
from fernet_fields import EncryptedCharField

class AuthMethod(BaseModel):
    BASIC = 'basic'
    KEY = 'key'
    TYPE_CHOICES = [
        (BASIC, 'Basic Authentication'),
        (KEY, 'Key Authentication'),
    ]

    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name='auth_methods')
    auth_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    priority = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        is_single_auth_method_for_api = Plan.objects.filter(api=api) and \
            (AuthMethod.objects.filter(api=self.api).count() == 1)

        if is_single_auth_method_for_api:
            raise IntegrityError('Cannot disable auth while billing plans exist')
        else:
            super(BaseCredentials, self).delete(*args, **kwargs)

    def __str__(self):
        return "{} API {} authentication".format(self.api.name, self.auth_type)

    class Meta:
        unique_together = ('api', 'auth_type')
        ordering = ['priority']

class BaseCredentials(BaseModel):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    api = models.ForeignKey(API, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        are_single_credenials_for_api = Subscription.objects\
            .filter(plan__api=self.api) and \
            (BaseCredentials.objects\
            .filter(consumer=self.consumer).count() == 1)

        if are_single_credenials_for_api:
            raise IntegrityError('Consumer must have credentials for an API while subscribed to it')
        else:
            super(BaseCredentials, self).delete(*args, **kwargs)

    def __str__(self):
        return "{} API credentials for consumer {}".format(self.api, self.consumer)

class BasicAuthCredentials(BaseCredentials):
    username = models.CharField(max_length=255, unique=True)
    password = EncryptedCharField(max_length=255)

    def __str__(self):
        return self.username

class KeyCredentials(BaseCredentials):
    key = EncryptedCharField(max_length=1024)

class AcceptedKeyParameter(BaseModel):
    HEADER = 'header'
    QUERY = 'query'
    PARAM_CHOICES = [
        (HEADER, 'Header Parameter'),
        (QUERY, 'Query Parameter'),
    ]
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    param_type = models.CharField(max_length=10, choices=PARAM_CHOICES)

    def __str__(self):
        return "{} parameter '{}'".format(self.param_type, self.name)

    class Meta:
        unique_together = ('api', 'name', 'param_type')
