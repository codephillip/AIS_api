# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-04 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='trigger',
            name='start',
            field=models.BooleanField(default=False),
        ),
    ]
