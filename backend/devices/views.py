import datetime
import boto3
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from .serializers import DeviceClaimSerializer, DeviceSerializer, MeasurementSerializer
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

class MeasurementPagination(PageNumberPagination):
    page_size = 10

class MeasurementListView(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    pagination_class = MeasurementPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        register_id = self.kwargs['register_id']
        return Measurement.objects.filter(device__register_id=register_id).order_by('-recorded_at')

@api_view(['GET'])
@permission_classes([AllowAny])
def get_unprocessed_measurement(request):
    print("Received request with headers:", request.headers)
    print("Received request with GET params:", request.GET)

    worker_secret = request.GET.get('worker_secret')
    recorded_after = request.GET.get('recorded_after')
    
    print("Worker secret:", worker_secret)
    print("Recorded after:", recorded_after)

    if worker_secret != settings.WORKER_SECRET:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        recorded_after_date = timezone.make_aware(timezone.datetime.fromisoformat(recorded_after))
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    measurement = Measurement.objects.filter(
        recorded_at__gt=recorded_after_date
    ).filter(
        Q(inference_value__isnull=True) | Q(inference_value='')
    ).order_by('-recorded_at').first()
    
    if not measurement:
        return Response({'message': 'No measurements found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MeasurementSerializer(measurement)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    data = serializer.data
    filename = data['value']
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600
        )
        data['presigned_url'] = presigned_url
    except (NoCredentialsError, PartialCredentialsError) as e:
        data['presigned_url'] = None

    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_inference_value(request):
    worker_secret = request.data.get('worker_secret')
    measurement_id = request.data.get('id')
    inference_value = request.data.get('inference_value')

    if worker_secret != settings.WORKER_SECRET:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        measurement = Measurement.objects.get(id=measurement_id)
        measurement.inference_value = inference_value
        measurement.save()
        return Response({'message': 'Inference value updated successfully'}, status=status.HTTP_200_OK)
    except Measurement.DoesNotExist:
        return Response({'error': 'Measurement not found'}, status=status.HTTP_404_NOT_FOUND)
