# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-27 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0004_experiment_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='in_process',
            field=models.BooleanField(default=False),
        ),
    ]
