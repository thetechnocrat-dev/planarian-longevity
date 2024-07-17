from django.db import migrations, models
import uuid

def generate_secrets(apps, schema_editor):
    Device = apps.get_model('devices', 'Device')
    for device in Device.objects.all():
        device.secret = str(uuid.uuid4())  # Generates a unique UUID for each device
        device.save()

class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_alter_device_device_type_alter_device_device_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='last_heartbeat',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='secret',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.RunPython(generate_secrets),
    ]
