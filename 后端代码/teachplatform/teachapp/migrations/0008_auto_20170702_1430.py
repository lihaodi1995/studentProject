# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0007_auto_20170702_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='team_lbound',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='course',
            name='team_ubound',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='team',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
