from django.urls import path
from .views import claim_device, DeviceListView, DeviceDetailView

urlpatterns = [
    path('claim/', claim_device, name='claim_device'),
    path('list-devices/', DeviceListView.as_view(), name='list-devices'),
    path('<str:register_id>/', DeviceDetailView.as_view(), name='device-detail'),
]
