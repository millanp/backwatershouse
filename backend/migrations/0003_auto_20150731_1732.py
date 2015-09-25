# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20150731_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='name',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
