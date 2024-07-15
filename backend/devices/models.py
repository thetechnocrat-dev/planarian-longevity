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

    def __str__(self):
        return f"{self.device_type} ({self.device_version}) - {self.register_id}"
