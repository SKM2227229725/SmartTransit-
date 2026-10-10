"""
ASGI entrypoint. Channels routing is added in PHASE 9.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

# PHASE 9 will add ProtocolTypeRouter + WebSocket consumers here
application = django_asgi_app