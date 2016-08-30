# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-30 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_remove_plan_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='max_evacuation_time',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Maximum Evacuation Time in Min'),
        ),
    ]
