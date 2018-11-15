# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0003_auto_20170701_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamhomework',
            name='times',
            field=models.IntegerField(default=1),
        ),
    ]
