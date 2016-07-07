# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-04 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0007_auto_20160215_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='max_evacuation_time',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='in minutes', null=True, verbose_name='Maximum Evacuation Time'),
        ),
        migrations.AlterField(
            model_name='floor',
            name='max_evacuation_time',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='in minutes', null=True, verbose_name='Maximum Evacuation Time'),
        ),
    ]