# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20150731_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='rooms',
        ),
        migrations.AddField(
            model_name='booking',
            name='rooms',
            field=multiselectfield.db.fields.MultiSelectField(default=b'None', max_length=5, choices=[(b'1', b'Room 1'), (b'2', b'Room 2'), (b'3', b'Room 3')]),
        ),
    ]
