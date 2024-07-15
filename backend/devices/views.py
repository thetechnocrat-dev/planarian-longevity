from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import DeviceClaimSerializer
from .models import Device

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_device(request):
    try:
        device = Device.objects.get(register_id=request.data['register_id'], registered=False)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found or already claimed'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DeviceClaimSerializer(device, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Device successfully claimed'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
