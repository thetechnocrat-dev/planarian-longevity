# Generated by Django 5.0.7 on 2024-08-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_measurement_inference_status_measurement_queued_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='mac_address',
            field=models.CharField(blank=True, max_length=17, null=True, unique=True),
        ),
    ]