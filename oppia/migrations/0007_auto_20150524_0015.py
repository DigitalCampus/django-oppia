# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0006_auto_20150401_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='oppia.Schedule', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='points',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='oppia.Course', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='oppia.Course', null=True),
            preserve_default=True,
        ),
    ]
