# Generated by Django 2.0.5 on 2018-07-01 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Meeting', '__first__'),
        ('User', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_1', models.CharField(max_length=20)),
                ('author_2', models.CharField(max_length=20, null=True)),
                ('author_3', models.CharField(max_length=20, null=True)),
                ('title', models.CharField(max_length=64)),
                ('abstract', models.CharField(max_length=1024, null=True)),
                ('keyword', models.CharField(max_length=128, null=True)),
                ('content', models.FileField(upload_to='paper/')),
                ('status', models.IntegerField()),
                ('meeting', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Meeting.Meeting')),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
    ]
