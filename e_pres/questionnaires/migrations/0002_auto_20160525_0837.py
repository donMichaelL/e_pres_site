# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-25 08:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EvaluationQuestionnaireAnswer',
            new_name='EvaluationQuestionnaireQuestion',
        ),
    ]