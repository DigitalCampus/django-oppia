# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='quiz.Quiz', null=True),
            preserve_default=True,
        ),
    ]
