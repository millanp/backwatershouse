# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20151108_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='stay',
            field=django.contrib.postgres.fields.ranges.DateRangeField(null=True, blank=True),
        ),
    ]
