# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-15 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_auto_20160218_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='leader',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]
