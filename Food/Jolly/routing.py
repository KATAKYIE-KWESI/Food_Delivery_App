from django.urls import re_path
from Jolly.consumers import DeliveryConsumer

websocket_urlpatterns = [
    re_path(r'ws/tracking/(?P<delivery_id>\d+)/$', DeliveryConsumer.as_asgi()),
]
