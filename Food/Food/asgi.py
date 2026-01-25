import os
import django
from django.core.asgi import get_asgi_application

# 1. Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Food.settings')
django.setup()

# 2. Import Channels and your app's routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# CHANGE THIS LINE: Remove "Food." from the front
from Jolly.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})