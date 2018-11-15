# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='semester',
            name='start_time',
            field=models.DateField(),
        ),
    ]
