# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-08 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20160708_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpointfailplan',
            name='last_current_checkpoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='experiments.Checkpoint'),
        ),
    ]
