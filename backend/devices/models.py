from django.db import models
from django.conf import settings
import uuid

class Device(models.Model):
    DEVICE_TYPES = (
        ('flatworm_watcher', 'Flatworm Watcher'),
    )

    DEVICE_VERSIONS = (
        ('flatworm_watcher_v1', 'Flatworm Watcher Version 1'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    register_id = models.CharField(max_length=6, unique=True)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    device_version = models.CharField(max_length=20, choices=DEVICE_VERSIONS)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.register_id} - {self.device_type} ({self.device_version})"

class Measurement(models.Model):
    SENSOR_TYPES = (
        ('camera', 'Camera'),
    )

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='datapoints', db_index=True)
    sensor = models.CharField(max_length=10, choices=SENSOR_TYPES)
    value = models.TextField()
    recorded_at = models.DateTimeField(db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.register_id} - {self.sensortype} - {self.recorded_at}"
