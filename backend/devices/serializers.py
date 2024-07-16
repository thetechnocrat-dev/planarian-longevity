from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Device


class DeviceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['register_id']
        extra_kwargs = {'register_id': {'validators': []}}  # Remove unique validator during update

    def update(self, instance, validated_data):
        instance.owner = self.context['request'].user
        instance.registered = True
        instance.save()
        return instance

class DeviceSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    lookup_field = 'register_id'

    class Meta:
        model = Device
        fields = ['uuid', 'register_id', 'device_type', 'device_version', 'owner', 'owner_username', 'registered', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at', 'owner_username']

    def create(self, validated_data):
        # Add custom creation logic if needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Add custom update logic if needed
        instance = super().update(instance, validated_data)
        instance.save()
        return instance
