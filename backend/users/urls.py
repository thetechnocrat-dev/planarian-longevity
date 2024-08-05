from django.urls import path
from .views import SignUpView, CustomTokenObtainPairView, GetPresignedUrlView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-presigned-url/<path:encoded_filename>/', GetPresignedUrlView.as_view(), name='get_presigned_url'),
]
