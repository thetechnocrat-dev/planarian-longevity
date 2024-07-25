from django.contrib import admin
from .models import Device, Measurement

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('register_id', 'device_type', 'device_version', 'owner', 'last_heartbeat', 'registered', 'created_at')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    fields = ('uuid', 'register_id', 'device_type', 'device_version', 'owner', 'last_heartbeat', 'registered', 'secret', 'created_at', 'updated_at')
    search_fields = ('register_id', 'device_type', 'device_version', 'owner__username')

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'sensor', 'recorded_at', 'uploaded_at', 'value', 'inference_value')
    list_filter = ('sensor', 'recorded_at')
    search_fields = ('device__register_id', 'value')

admin.site.register(Device, DeviceAdmin)
admin.site.register(Measurement, MeasurementAdmin)

