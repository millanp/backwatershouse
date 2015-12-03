# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20151130_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='approval_state',
            field=models.PositiveSmallIntegerField(default=4, choices=[(1, b'Awaiting owner approval'), (2, b'Payment required'), (3, b'Booking is paid for and complete'), (4, b'Booking is complete')]),
            preserve_default=False,
        ),
    ]
