# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0005_coursecohort'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursecohort',
            unique_together=set([('course', 'cohort')]),
        ),
    ]
