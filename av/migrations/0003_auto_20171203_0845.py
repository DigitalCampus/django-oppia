# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0002_auto_20170214_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedmedia',
            name='course_shortname',
        ),
        migrations.RemoveField(
            model_name='uploadedmedia',
            name='image',
        ),
    ]
