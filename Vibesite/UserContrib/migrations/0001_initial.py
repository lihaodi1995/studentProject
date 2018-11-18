# Generated by Django 2.0.6 on 2018-07-02 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ConfManage', '0001_initial'),
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('contribution_id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.CharField(choices=[('g', 'Granted'), ('r', 'Rejected'), ('p', 'Pending')], default='p', max_length=1)),
                ('comment', models.CharField(max_length=2048, null=True)),
                ('modified_times', models.IntegerField(default=0)),
                ('last_modified', models.DateTimeField(verbose_name='modified')),
                ('author', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=255)),
                ('organization', models.CharField(max_length=32, null=True)),
                ('abstract', models.CharField(max_length=1024)),
                ('url', models.CharField(max_length=64)),
                ('register_status', models.BooleanField(default=False)),
                ('conference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ConfManage.Conference')),
                ('contib_reg', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ConfManage.ConferenceRegistration')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserAuth.User')),
            ],
        ),
    ]