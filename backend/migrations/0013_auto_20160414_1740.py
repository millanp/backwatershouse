# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20151206_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='approval_state',
            field=models.PositiveSmallIntegerField(choices=[(1, b'Awaiting owner approval'), (2, b'Approved; waiting for payment'), (3, b'Paid for, finalized, and scheduled'), (4, b'Finalized and scheduled'), (5, b'Rejected')], default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='arrive',
            field=models.DateField(verbose_name=b'Arrival'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='extra',
            field=models.BooleanField(default=False, verbose_name=b'Housekeeping services desired'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='leave',
            field=models.DateField(verbose_name=b'Departure'),
        ),
    ]
