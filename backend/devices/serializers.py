from rest_framework import serializers
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
