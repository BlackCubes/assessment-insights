import os

from django.core.asgi import get_asgi_application

DJANGO_SETTINGS_MODULE = (
    "config.settings.dev"
    if (os.getenv("DEBUG", "True") == "True")
    else "config.settings.prod"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

application = get_asgi_application()
