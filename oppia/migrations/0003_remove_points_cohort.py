# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0002_remove_cohort_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='points',
            name='cohort',
        ),
    ]
