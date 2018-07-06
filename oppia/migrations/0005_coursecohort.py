# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0004_auto_20150329_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cohort', models.ForeignKey(to='oppia.Cohort', on_delete=models.CASCADE)),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model, ),
        ),
    ]
