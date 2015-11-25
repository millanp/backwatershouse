# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20151109_0118'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='booking',
            name='booking_event_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='request_event_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='booking_cal_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='request_cal_id',
            field=models.TextField(null=True, blank=True),
        ),
    ]
