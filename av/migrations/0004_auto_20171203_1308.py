# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0003_auto_20171203_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedmedia',
            name='file',
            field=models.FileField(upload_to=b'uploaded/%Y/%m/'),
        ),
    ]
