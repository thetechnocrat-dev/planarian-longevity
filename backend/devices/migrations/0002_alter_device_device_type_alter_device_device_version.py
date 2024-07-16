# Generated by Django 5.0.7 on 2024-07-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(choices=[('flatworm_watcher', 'Flatworm Watcher')], max_length=50),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_version',
            field=models.CharField(choices=[('flatworm_watcher_v1', 'Flatworm Watcher Version 1')], max_length=20),
        ),
    ]