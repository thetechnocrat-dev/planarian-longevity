from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Message
from .serializers import MessageSerializer
from devices.models import Device

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_message(request):
    user = request.user
    device_type = request.data.get('device_type')
    content = request.data.get('content')

    if not device_type or not content:
        return Response({'error': 'Device type and content are required'}, status=400)

    if not Device.objects.filter(owner=user, device_type=device_type).exists():
        return Response({'error': 'User does not own a device of this type'}, status=403)

    message = Message.objects.create(user=user, device_type=device_type, content=content)
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=201)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        device_type = self.request.query_params.get('device_type')

        if not Device.objects.filter(owner=user, device_type=device_type).exists():
            return Message.objects.none()

        return Message.objects.filter(device_type=device_type).order_by('-created_at')
