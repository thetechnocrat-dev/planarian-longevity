import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.http import JsonResponse
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from urllib.parse import unquote


class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(email=response.data['email'])
        refresh = RefreshToken.for_user(user)
        response.data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class GetPresignedUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, encoded_filename):
        filename = unquote(encoded_filename)
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        try:
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': filename},
                ExpiresIn=3600
            )
            return JsonResponse({'url': presigned_url})
        except (NoCredentialsError, PartialCredentialsError) as e:
            return JsonResponse({'error': str(e)}, status=403)
