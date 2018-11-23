# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_shortname', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('lastupdated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated')),
                ('file', models.FileField(upload_to=b'uploaded')),
                ('image', models.FileField(default=None, upload_to=b'uploaded', blank=True)),
                ('md5', models.CharField(max_length=100)),
                ('length', models.IntegerField(default=0, blank=True)),
                ('create_user', models.ForeignKey(related_name='media_create_user', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('update_user', models.ForeignKey(related_name='media_update_user', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Uploaded Media',
                'verbose_name_plural': 'Uploaded Media',
            },
        ),
    ]
