# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20150804_1534'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='extra',
        ),
        migrations.AddField(
            model_name='booking',
            name='extra',
            field=multiselectfield.db.fields.MultiSelectField(default=b'None', max_length=5, choices=[(b'1', b'Extra1'), (b'2', b'Extra2'), (b'3', b'Extra3')]),
        ),
        migrations.DeleteModel(
            name='Extra',
        ),
    ]
