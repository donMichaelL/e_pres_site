# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-16 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0005_auto_20160830_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='sequence',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]