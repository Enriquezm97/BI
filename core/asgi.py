import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()
#django_asgi_app = get_asgi_application()

#application = ProtocolTypeRouter({
#    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
#})