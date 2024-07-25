from django.urls import path
from .views import create_message, MessageListView

urlpatterns = [
    path('create/', create_message, name='create_message'),
    path('list/', MessageListView.as_view(), name='list_messages'),
]
