# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-29 12:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0008_checkpoint_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkpoint',
            old_name='order',
            new_name='sequence',
        ),
    ]
