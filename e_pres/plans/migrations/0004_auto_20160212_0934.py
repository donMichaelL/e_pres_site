# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-12 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_plan_max_evacuation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='max_evacuation_time',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Maximum Evacuation Time in Sec'),
        ),
    ]