from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.relations import HyperlinkedIdentityField

from api_logging.models import APILogEntry

class HyperlinkedChildField(HyperlinkedIdentityField):

    # view_name argument is required
    # http://www.django-rest-framework.org/api-guide/relations/#hyperlinkedidentityfield
    def __init__(self, parent, *args, **kwargs):
        self.lookup_fields = ((parent+'_id', parent+'_pk'), ('id', 'pk'))
        super(HyperlinkedChildField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = {}
        for model_field, url_param in self.lookup_fields:
            attr = obj
            for field in model_field.split('.'):
                attr = getattr(attr,field)
            kwargs[url_param] = attr

        return reverse(view_name, kwargs=kwargs, request=request, format=format)

class MoneyField(models.DecimalField):
     def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 8
        kwargs['decimal_places'] = 2
        super(MoneyField, self).__init__(*args, **kwargs)
