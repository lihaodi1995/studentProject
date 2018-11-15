# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teachapp', '0009_auto_20170704_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_a', models.ForeignKey(related_name='user_a', to='teachapp.User')),
                ('user_b', models.ForeignKey(related_name='user_b', to='teachapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='judge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
