# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0008_auto_20170702_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
