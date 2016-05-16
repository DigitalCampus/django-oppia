# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0003_auto_20160510_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingProperties',
            fields=[
                ('key', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('str_value', models.CharField(max_length=50, null=True, blank=True)),
                ('int_value', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='coursedailystats',
            unique_together=set([('course', 'day', 'type')]),
        ),
        migrations.AlterIndexTogether(
            name='coursedailystats',
            index_together=set([('course', 'day', 'type')]),
        ),
        migrations.RemoveField(
            model_name='coursedailystats',
            name='completed_activities',
        ),
        migrations.RemoveField(
            model_name='coursedailystats',
            name='media_viewed',
        ),
        migrations.RemoveField(
            model_name='coursedailystats',
            name='quizzes_passed',
        ),
        migrations.RemoveField(
            model_name='coursedailystats',
            name='resources_viewed',
        ),
    ]
