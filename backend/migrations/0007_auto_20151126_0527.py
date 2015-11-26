# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20151125_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='request_event_id',
        ),
    ]
