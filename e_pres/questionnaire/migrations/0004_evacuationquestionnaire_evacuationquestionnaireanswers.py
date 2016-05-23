# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-23 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0007_auto_20160215_1412'),
        ('questionnaire', '0003_auto_20160523_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvacuationQuestionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='buildings.Building')),
            ],
        ),
        migrations.CreateModel(
            name='EvacuationQuestionnaireAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], max_length=3)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.EvaluationQuestionnaireQuestion')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.EvacuationQuestionnaire')),
            ],
        ),
    ]