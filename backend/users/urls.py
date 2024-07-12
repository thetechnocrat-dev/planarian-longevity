from django.urls import path
from .views import SignUpView, CustomTokenObtainPairView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]