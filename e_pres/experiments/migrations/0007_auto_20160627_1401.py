# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-27 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0006_auto_20160627_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='evacuation_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='expected_evacuation_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='starting_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
