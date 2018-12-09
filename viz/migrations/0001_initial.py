# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserLocationVisualization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
                ('hits', models.IntegerField(default=0)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('region', models.TextField(blank=True)),
                ('country_code', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('country_name', models.TextField(default=None, null=True, blank=True)),
                ('geonames_data', models.TextField(default=None, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model, ),
        ),
    ]
