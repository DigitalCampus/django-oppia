# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedailystats',
            name='course',
            field=models.ForeignKey(default=None, blank=True, to='oppia.Course', null=True, on_delete=models.CASCADE),
        ),
    ]
