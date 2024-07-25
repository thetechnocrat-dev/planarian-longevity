from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['username', 'device_type', 'created_at', 'content']

    def get_username(self, obj):
        return obj.user.username
