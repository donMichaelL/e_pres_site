# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]
