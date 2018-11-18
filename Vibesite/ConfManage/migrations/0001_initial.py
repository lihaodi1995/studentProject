# Generated by Django 2.0.6 on 2018-07-02 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GroupAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('conf_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('introduction', models.CharField(max_length=255)),
                ('contribution_deadline', models.DateTimeField(verbose_name='ddl')),
                ('inform_date', models.DateTimeField(verbose_name='inform')),
                ('register_date', models.DateTimeField(verbose_name='reg')),
                ('conference_date', models.DateTimeField(verbose_name='conf')),
                ('arrangement', models.CharField(max_length=255, null=True)),
                ('fee', models.IntegerField(default=0, null=True)),
                ('logistics', models.CharField(help_text='transportations and accomodations', max_length=255, null=True)),
                ('contact', models.CharField(max_length=32, null=True)),
                ('template', models.IntegerField(default=0, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='GroupAuth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('registration_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('a', 'Audit'), ('p', 'Participate')], default='a', max_length=1)),
                ('result', models.CharField(choices=[('g', 'Granted'), ('r', 'Rejected'), ('p', 'Pending')], default='p', max_length=1)),
                ('real_name', models.CharField(max_length=32)),
                ('user_gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], default='m', max_length=1)),
                ('accomodation', models.BooleanField(default=False)),
                ('payment', models.CharField(help_text='url', max_length=64, null=True)),
            ],
        ),
    ]
