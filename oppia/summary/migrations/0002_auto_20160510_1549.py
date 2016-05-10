# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursedailystats',
            options={'verbose_name': 'CourseDailyStats'},
        ),
        migrations.AlterModelOptions(
            name='usercoursesummary',
            options={'verbose_name': 'UserCourseSummary'},
        ),
        migrations.AlterUniqueTogether(
            name='coursedailystats',
            unique_together=set([('course', 'day')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercoursesummary',
            unique_together=set([('user', 'course')]),
        ),
        migrations.AlterIndexTogether(
            name='coursedailystats',
            index_together=set([('course', 'day')]),
        ),
        migrations.AlterIndexTogether(
            name='usercoursesummary',
            index_together=set([('user', 'course')]),
        ),
    ]
