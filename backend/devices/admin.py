from django.contrib import admin
from .models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('register_id', 'device_type', 'device_version', 'owner', 'last_heartbeat', 'registered', 'created_at')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    fields = ('uuid', 'register_id', 'device_type', 'device_version', 'owner', 'last_heartbeat', 'registered', 'secret', 'created_at', 'updated_at')
    search_fields = ('register_id', 'device_type', 'device_version', 'owner__username')

admin.site.register(Device, DeviceAdmin)
