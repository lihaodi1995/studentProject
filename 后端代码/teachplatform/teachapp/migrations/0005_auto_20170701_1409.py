# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0004_teamhomework_times'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamhomework',
            name='done',
        ),
        migrations.AddField(
            model_name='weight',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
