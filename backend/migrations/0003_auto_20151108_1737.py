# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20151027_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='arrive',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='leave',
        ),
        migrations.AddField(
            model_name='booking',
            name='stay',
            field=django.contrib.postgres.fields.ranges.DateRangeField(null=True),
        ),
    ]
