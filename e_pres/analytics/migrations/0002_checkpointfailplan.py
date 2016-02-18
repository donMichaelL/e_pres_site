# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-18 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_auto_20160218_1243'),
        ('experiments', '0003_auto_20160202_1130'),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckpointFailPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.IntegerField()),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Experiment')),
                ('last_current_checkpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.Checkpoint')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plans.Plan')),
            ],
        ),
    ]
