# Generated by Django 5.0.7 on 2024-07-30 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_measurement_inference_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='inference_status',
            field=models.CharField(choices=[('not_selected', 'Not Selected'), ('selected', 'Selected'), ('processing', 'Processing'), ('failed', 'Failed'), ('succeeded', 'Succeeded')], default='not_selected', max_length=20),
        ),
        migrations.AddField(
            model_name='measurement',
            name='queued_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]