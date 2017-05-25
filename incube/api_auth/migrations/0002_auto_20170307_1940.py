# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_api_consumer'),
        ('api_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecredentials',
            name='api',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.API'),
        ),
        migrations.AddField(
            model_name='basecredentials',
            name='consumer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Consumer'),
        ),
        migrations.AddField(
            model_name='authmethod',
            name='api',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_methods', to='core.API'),
        ),
        migrations.AddField(
            model_name='acceptedkeyparameter',
            name='api',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.API'),
        ),
        migrations.AlterUniqueTogether(
            name='authmethod',
            unique_together=set([('api', 'auth_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='acceptedkeyparameter',
            unique_together=set([('api', 'name', 'param_type')]),
        ),
    ]
