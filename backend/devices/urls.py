from django.urls import path
from .views import claim_device

urlpatterns = [
    path('claim/', claim_device, name='claim_device'),
]
