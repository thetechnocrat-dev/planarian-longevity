from django.urls import path
from .views import SignUpView, CustomTokenObtainPairView, GetPresignedUrlView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('get-presigned-url/<path:encoded_filename>/', GetPresignedUrlView.as_view(), name='get_presigned_url'),
]