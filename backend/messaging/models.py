from django.db import models
from django.conf import settings
from devices.choices import DEVICE_TYPES

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.TextField()

    def __str__(self):
        return f"Message from {self.user} about {self.device_type} at {self.created_at}"
