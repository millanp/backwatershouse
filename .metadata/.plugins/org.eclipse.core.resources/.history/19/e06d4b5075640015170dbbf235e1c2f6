# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arrive', models.DateField()),
                ('leave', models.DateField()),
                ('approved', models.BooleanField(default=False)),
                ('payment_required', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1, choices=[(b'1', b'Extra 1'), (b'2', b'Extra 2'), (b'3', b'Extra 3')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1, choices=[(b'1', b'Room 1'), (b'2', b'Room 2'), (b'3', b'Room 3'), (b'4', b'Room 4')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking',
            name='extra',
            field=models.ManyToManyField(to='backend.Extra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='guest',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='rooms',
            field=models.ManyToManyField(to='backend.Room'),
            preserve_default=True,
        ),
    ]
