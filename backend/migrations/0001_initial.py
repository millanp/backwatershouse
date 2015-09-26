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
                ('extra', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('payment_required', models.BooleanField(default=False)),
                ('paid_for', models.BooleanField(default=True)),
                ('guest', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField()),
                ('blurb', models.TextField(max_length=700)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='rooms',
            field=models.ManyToManyField(to='backend.Room'),
        ),
    ]
