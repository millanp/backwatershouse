# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20151108_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='arrive',
            field=models.DateField(default=datetime.datetime(2015, 9, 7, 0, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='leave',
            field=models.DateField(default=datetime.datetime(2015, 10, 7, 0, 0)),
            preserve_default=False,
        ),
    ]
