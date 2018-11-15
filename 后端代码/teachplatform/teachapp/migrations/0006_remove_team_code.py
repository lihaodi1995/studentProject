# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0005_auto_20170701_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='code',
        ),
    ]
