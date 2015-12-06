# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20151206_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='approval_state',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'Awaiting owner approval'), (2, b'Waiting for payment'), (3, b'Booking is paid for and complete'), (4, b'Booking is complete')]),
        ),
    ]
