# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0006_remove_team_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='team_ddl',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='team',
            name='code',
            field=models.IntegerField(null=True),
        ),
    ]
