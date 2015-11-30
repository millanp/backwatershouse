# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20151126_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_event_ids',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={}, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='request_event_ids',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={}, blank=True),
        ),
    ]
