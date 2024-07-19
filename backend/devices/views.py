import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import DeviceClaimSerializer, DeviceSerializer, MeasurementSerializer, MeasurementPagination
from .models import Device, Measurement


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

class DeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Device.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        your_devices = queryset.filter(owner=request.user)
        other_devices = queryset.exclude(owner=request.user)

        return Response({
            'your_devices': DeviceSerializer(your_devices, many=True).data,
            'other_devices': DeviceSerializer(other_devices, many=True).data
        })

class DeviceDetailView(RetrieveAPIView):
    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceSerializer
    lookup_field = 'register_id'

class HeartbeatView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, register_id, format=None):
        secret = request.data.get('secret')
        try:
            device = Device.objects.get(register_id=register_id, secret=secret)
            device.last_heartbeat = timezone.now()
            device.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({'error': 'Invalid device or secret'}, status=status.HTTP_400_BAD_REQUEST)

class MeasurementUploadView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, register_id):
        secret = request.data.get('secret')
        file = request.data.get('file')
        recorded_at = request.data.get('recorded_at')
        sensor = request.data.get('sensor')

        try:
            device = Device.objects.get(register_id=register_id, secret=secret)

            # Assuming filename is formatted as YYYYMMDD_HHMMSS_sensor.ext
            path = default_storage.save(f'{device.uuid}/{sensor}/{str(file)}', ContentFile(file.read()))

            measurement = Measurement.objects.create(
                device=device,
                sensor=sensor,
                value=path,
                recorded_at=datetime.datetime.strptime(recorded_at, '%Y-%m-%dT%H:%M:%SZ'),
                uploaded_at=datetime.datetime.now()
            )
            return Response({'status': 'success', 'path': path}, status=status.HTTP_201_CREATED)
        except Device.DoesNotExist:
            return Response({'error': 'Invalid device or secret'}, status=status.HTTP_400_BAD_REQUEST)

class MeasurementListView(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    pagination_class = MeasurementPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        register_id = self.kwargs['register_id']
        return Measurement.objects.filter(device__register_id=register_id).order_by('-recorded_at')
