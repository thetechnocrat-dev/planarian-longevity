# Generated by Django 5.0.7 on 2024-07-23 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_measurement'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='inference_value',
            field=models.TextField(blank=True, null=True),
        ),
    ]