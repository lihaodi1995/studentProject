# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=24)),
                ('code', models.CharField(unique=True, max_length=8)),
                ('credit', models.IntegerField()),
                ('start_week', models.IntegerField()),
                ('end_week', models.IntegerField()),
                ('info', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='teachapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=24)),
                ('content', models.TextField(null=True)),
                ('score', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('times', models.IntegerField()),
                ('course', models.ForeignKey(to='teachapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=24)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('weeks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='teachapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=16)),
                ('verified', models.BooleanField(default=False)),
                ('members', models.IntegerField(default=1)),
                ('course', models.ForeignKey(to='teachapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='TeamHomework',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(null=True)),
                ('time', models.DateTimeField()),
                ('score', models.IntegerField(null=True)),
                ('comment', models.TextField(null=True)),
                ('done', models.IntegerField(default=0)),
                ('homework', models.ForeignKey(to='teachapp.Homework')),
                ('team', models.ForeignKey(to='teachapp.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=16)),
                ('verified', models.BooleanField(default=False)),
                ('student', models.ForeignKey(to='teachapp.Student')),
                ('team', models.ForeignKey(to='teachapp.Team')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=16)),
                ('password', models.CharField(default='000000', max_length=128)),
                ('name', models.CharField(max_length=8)),
                ('email', models.CharField(max_length=48, unique=True, null=True)),
                ('phone', models.CharField(max_length=11, unique=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('student', models.ForeignKey(to='teachapp.Student')),
                ('teamhomework', models.ForeignKey(to='teachapp.TeamHomework')),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.ForeignKey(to='teachapp.User'),
        ),
        migrations.AddField(
            model_name='teach',
            name='teacher',
            field=models.ForeignKey(to='teachapp.Teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(to='teachapp.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='user_from',
            field=models.ForeignKey(related_name='user_from', to='teachapp.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='user_to',
            field=models.ForeignKey(related_name='user_to', to='teachapp.User'),
        ),
        migrations.AddField(
            model_name='enroll',
            name='student',
            field=models.ForeignKey(to='teachapp.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(to='teachapp.Semester'),
        ),
        migrations.AddField(
            model_name='admin',
            name='user',
            field=models.ForeignKey(to='teachapp.User'),
        ),
    ]
