# Generated by Django 5.0.7 on 2024-07-17 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_device_last_heartbeat_device_secret'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor', models.CharField(choices=[('camera', 'Camera')], max_length=10)),
                ('value', models.TextField()),
                ('recorded_at', models.DateTimeField(db_index=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datapoints', to='devices.device')),
            ],
        ),
    ]