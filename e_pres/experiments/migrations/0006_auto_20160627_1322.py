# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-27 13:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0005_experiment_in_process'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='in_process',
            new_name='in_progress',
        ),
    ]