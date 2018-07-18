# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20150524_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='ip',
            field=models.GenericIPAddressField(),
            preserve_default=True,
        ),
    ]
