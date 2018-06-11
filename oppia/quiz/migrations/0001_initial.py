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
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('lastupdated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated')),
                ('title', models.TextField()),
                ('type', models.CharField(default=b'multichoice', max_length=15, choices=[(b'multichoice', b'Multiple choice'), (b'shortanswer', b'Short answer'), (b'matching', b'Matching'), (b'numerical', b'Numerical'), (b'multiselect', b'Multiple select'), (b'description', b'Information only'), (b'essay', b'Essay question')])),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='QuestionProps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('value', models.TextField(blank=True)),
                ('question', models.ForeignKey(to='quiz.Question', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'QuestionProp',
                'verbose_name_plural': 'QuestionProps',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('lastupdated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated')),
                ('draft', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attempt_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date attempted')),
                ('submitted_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date submitted')),
                ('score', models.DecimalField(max_digits=6, decimal_places=2)),
                ('maxscore', models.DecimalField(max_digits=6, decimal_places=2)),
                ('ip', models.IPAddressField()),
                ('instance_id', models.CharField(max_length=50, null=True, blank=True)),
                ('agent', models.TextField(blank=True)),
                ('quiz', models.ForeignKey(to='quiz.Quiz', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'QuizAttempt',
                'verbose_name_plural': 'QuizAttempts',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='QuizAttemptResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(max_digits=6, decimal_places=2)),
                ('text', models.TextField(blank=True)),
                ('question', models.ForeignKey(to='quiz.Question', on_delete=models.CASCADE)),
                ('quizattempt', models.ForeignKey(to='quiz.QuizAttempt', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'QuizAttemptResponse',
                'verbose_name_plural': 'QuizAttemptResponses',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='QuizProps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('value', models.TextField(blank=True)),
                ('quiz', models.ForeignKey(to='quiz.Quiz', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'QuizProp',
                'verbose_name_plural': 'QuizProps',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=1)),
                ('question', models.ForeignKey(to='quiz.Question', on_delete=models.CASCADE)),
                ('quiz', models.ForeignKey(to='quiz.Quiz', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'QuizQuestion',
                'verbose_name_plural': 'QuizQuestions',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('lastupdated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated')),
                ('score', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('title', models.TextField()),
                ('order', models.IntegerField(default=1)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('question', models.ForeignKey(to='quiz.Question', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Response',
                'verbose_name_plural': 'Responses',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='ResponseProps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('value', models.TextField(blank=True)),
                ('response', models.ForeignKey(to='quiz.Response', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'ResponseProp',
                'verbose_name_plural': 'ResponseProps',
            },
            bases=(models.Model, ),
        ),
        migrations.AddField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(to='quiz.Question', through='quiz.QuizQuestion'),
            preserve_default=True,
        ),
    ]
