# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-23 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('buildings', '0007_auto_20160215_1412'),
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
            name='EvacuationQuestionnaireAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationQuestionnaireQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=240)),
            ],
        ),
        migrations.AddField(
            model_name='evacuationquestionnaireanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaires.EvaluationQuestionnaireQuestion'),
        ),
        migrations.AddField(
            model_name='evacuationquestionnaireanswer',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaires.EvacuationQuestionnaire'),
        ),
        migrations.AlterUniqueTogether(
            name='evacuationquestionnaireanswer',
            unique_together=set([('questionnaire', 'question')]),
        ),
    ]