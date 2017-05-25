# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20170307_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='overage_call_cost',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='enable_overage',
            field=models.BooleanField(default=False),
        ),
    ]
