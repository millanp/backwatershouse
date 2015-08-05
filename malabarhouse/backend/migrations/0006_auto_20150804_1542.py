# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20150804_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='extra',
            field=multiselectfield.db.fields.MultiSelectField(default=b'-', max_length=5, choices=[(b'1', b'Extra1'), (b'2', b'Extra2'), (b'3', b'Extra3')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='rooms',
            field=multiselectfield.db.fields.MultiSelectField(default=b'-', max_length=5, choices=[(b'1', b'Room 1'), (b'2', b'Room 2'), (b'3', b'Room 3')]),
        ),
    ]
