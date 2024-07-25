import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.http import JsonResponse
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer
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
        response.data['token'] = str(refresh.access_token)
        return response

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }
        user = authenticate(**authenticate_kwargs)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        refresh = self.get_token(user)
        return {
            'token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
            }
        }

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
            region_name=settings.AWS_REGION_NAME
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
