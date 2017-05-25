from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import BaseModel

from fernet_fields import EncryptedTextField

class StripeAccount(BaseModel):
    stripe_id = models.CharField(max_length=128)
    pub_key = models.CharField(max_length=1024)
    access_token = EncryptedTextField()
    refresh_token = EncryptedTextField()

    def __str__(self):
        return self.stripe_id

class User(AbstractUser):
    stripe_account = models.OneToOneField(StripeAccount, null=True)

    def __str__(self):
        return self.username
