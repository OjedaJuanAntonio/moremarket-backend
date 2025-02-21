
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moremarket.settings')
print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import gestionSubastas.routing
# import chat.routing



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # chat.routing.websocket_urlpatterns + gestionSubastas.routing.websocket_urlpatterns
            gestionSubastas.routing.websocket_urlpatterns
        )
    ),
})
