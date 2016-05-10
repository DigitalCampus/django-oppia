# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0010_move_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDailyStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField()),
                ('type', models.CharField(default=None, max_length=10, null=True, blank=True)),
                ('total', models.IntegerField(default=0)),
                ('quizzes_passed', models.IntegerField(default=0)),
                ('completed_activities', models.IntegerField(default=0)),
                ('media_viewed', models.IntegerField(default=0)),
                ('resources_viewed', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='oppia.Course')),
            ],
        ),
        migrations.CreateModel(
            name='UserCourseSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField(default=0)),
                ('total_downloads', models.IntegerField(default=0)),
                ('total_activity', models.IntegerField(default=0)),
                ('quizzes_passed', models.IntegerField(default=0)),
                ('badges_achieved', models.IntegerField(default=0)),
                ('pretest_score', models.FloatField(default=0)),
                ('media_viewed', models.IntegerField(default=0)),
                ('completed_activities', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='oppia.Course')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
