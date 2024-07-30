from django.urls import path
from .views import claim_device, DeviceListView, DeviceDetailView, HeartbeatView, MeasurementUploadView, MeasurementListView, get_unprocessed_measurement, update_inference_value, update_inference_status

urlpatterns = [
    path('claim/', claim_device, name='claim_device'),
    path('get_unprocessed_measurement/', get_unprocessed_measurement, name='get_unprocessed_measurement'),
    path('update_inference_value/', update_inference_value, name='update_inference_value'),
    path('update_inference_status/', update_inference_status, name='update_inference_status'),
    path('list-devices/', DeviceListView.as_view(), name='list-devices'),
    path('<str:register_id>/', DeviceDetailView.as_view(), name='device-detail'),
    path('<str:register_id>/heartbeat/', HeartbeatView.as_view(), name='device-heartbeat'),
    path('<str:register_id>/upload/', MeasurementUploadView.as_view(), name='measurement-upload'),
    path('<str:register_id>/measurements/', MeasurementListView.as_view(), name='measurement-list'),
]
