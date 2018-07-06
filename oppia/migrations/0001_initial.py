# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('title', models.TextField()),
                ('type', models.CharField(max_length=10)),
                ('digest', models.CharField(max_length=100)),
                ('baseline', models.BooleanField(default=False)),
                ('image', models.TextField(default=None, null=True, blank=True)),
                ('content', models.TextField(default=None, null=True, blank=True)),
                ('description', models.TextField(default=None, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='ActivitySchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('digest', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'ActivitySchedule',
                'verbose_name_plural': 'ActivitySchedules',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('award_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date awarded')),
            ],
            options={
                'verbose_name': 'Award',
                'verbose_name_plural': 'Awards',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='AwardCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_version', models.BigIntegerField(default=0)),
                ('award', models.ForeignKey(to='oppia.Award', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(max_length=20)),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('default_icon', models.FileField(upload_to=b'badges')),
                ('points', models.IntegerField(default=100)),
                ('allow_multiple_awards', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Badge',
                'verbose_name_plural': 'Badges',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Cohort',
                'verbose_name_plural': 'Cohorts',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('lastupdated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated')),
                ('version', models.BigIntegerField()),
                ('title', models.TextField()),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('shortname', models.CharField(max_length=20)),
                ('filename', models.CharField(max_length=200)),
                ('badge_icon', models.FileField(default=None, upload_to=b'badges', blank=True)),
                ('is_draft', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
            bases=(models.Model, ),
        ),
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
        migrations.CreateModel(
            name='CourseManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Course Manager',
                'verbose_name_plural': 'Course Managers',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='CourseTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Course Tag',
                'verbose_name_plural': 'Course Tags',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('digest', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=200)),
                ('download_url', models.URLField()),
                ('filesize', models.BigIntegerField(default=None, null=True, blank=True)),
                ('media_length', models.IntegerField(default=None, null=True, blank=True)),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.CharField(max_length=200)),
                ('link', models.URLField(max_length=255)),
                ('icon', models.CharField(max_length=200)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=20, choices=[(b'teacher', b'Teacher'), (b'student', b'Student')])),
                ('cohort', models.ForeignKey(to='oppia.Cohort', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('description', models.TextField()),
                ('data', models.TextField(blank=True)),
                ('type', models.CharField(max_length=20, choices=[(b'signup', b'Sign up'), (b'userquizattempt', b'Quiz attempt by user'), (b'firstattempt', b'First quiz attempt'), (b'firstattemptscore', b'First attempt score'), (b'firstattemptbonus', b'Bonus for first attempt score'), (b'quizattempt', b'Quiz attempt'), (b'quizcreated', b'Created quiz'), (b'activitycompleted', b'Activity completed'), (b'mediaplayed', b'Media played'), (b'badgeawarded', b'Badge awarded'), (b'coursedownloaded', b'Course downloaded')])),
                ('cohort', models.ForeignKey(to='oppia.Cohort', null=True, on_delete=models.CASCADE)),
                ('course', models.ForeignKey(to='oppia.Course', null=True, on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Points',
                'verbose_name_plural': 'Points',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('default', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('lastupdated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated')),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('title', models.TextField()),
                ('course', models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('order_priority', models.IntegerField(default=0)),
                ('highlight', models.BooleanField(default=False)),
                ('icon', models.FileField(default=None, null=True, upload_to=b'tags', blank=True)),
                ('courses', models.ManyToManyField(to='oppia.Course', through='oppia.CourseTag')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date submitted')),
                ('tracker_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date tracked')),
                ('ip', models.IPAddressField()),
                ('agent', models.TextField(blank=True)),
                ('digest', models.CharField(max_length=100)),
                ('data', models.TextField(blank=True)),
                ('type', models.CharField(default=None, max_length=10, null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('time_taken', models.IntegerField(default=0)),
                ('activity_title', models.TextField(default=None, null=True, blank=True)),
                ('section_title', models.TextField(default=None, null=True, blank=True)),
                ('uuid', models.TextField(default=None, null=True, blank=True)),
                ('lang', models.CharField(default=None, max_length=10, null=True, blank=True)),
                ('course', models.ForeignKey(default=None, blank=True, to='oppia.Course', null=True, on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Tracker',
                'verbose_name_plural': 'Trackers',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(default=None, null=True, blank=True)),
                ('can_upload', models.BooleanField(default=False)),
                ('job_title', models.TextField(default=None, null=True, blank=True)),
                ('organisation', models.TextField(default=None, null=True, blank=True)),
                ('phone_number', models.TextField(default=None, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model, ),
        ),
        migrations.AddField(
            model_name='coursetag',
            name='tag',
            field=models.ForeignKey(to='oppia.Tag', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cohort',
            name='course',
            field=models.ForeignKey(blank=True, to='oppia.Course', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cohort',
            name='schedule',
            field=models.ForeignKey(default=None, blank=True, to='oppia.Schedule', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awardcourse',
            name='course',
            field=models.ForeignKey(to='oppia.Course', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='award',
            name='badge',
            field=models.ForeignKey(to='oppia.Badge', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='award',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activityschedule',
            name='schedule',
            field=models.ForeignKey(to='oppia.Schedule', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='section',
            field=models.ForeignKey(to='oppia.Section', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
