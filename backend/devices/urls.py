from django.urls import path
from .views import claim_device, DeviceListView, DeviceDetailView, HeartbeatView, MeasurementUploadView

urlpatterns = [
    path('claim/', claim_device, name='claim_device'),
    path('list-devices/', DeviceListView.as_view(), name='list-devices'),
    path('<str:register_id>/', DeviceDetailView.as_view(), name='device-detail'),
    path('<str:register_id>/heartbeat/', HeartbeatView.as_view(), name='device-heartbeat'),
    path('<str:register_id>/upload/', MeasurementUploadView.as_view(), name='measurement-upload'),
]
