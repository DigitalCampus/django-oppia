# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0003_remove_points_cohort'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursecohort',
            name='cohort',
        ),
        migrations.RemoveField(
            model_name='coursecohort',
            name='course',
        ),
        migrations.DeleteModel(
            name='CourseCohort',
        ),
    ]
