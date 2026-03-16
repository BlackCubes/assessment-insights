import os

from django.core.wsgi import get_wsgi_application

DJANGO_SETTINGS_MODULE = (
    "config.settings.dev"
    if (os.getenv("DEBUG", "TRUE") == "TRUE")
    else "config.settings.prod"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

application = get_wsgi_application()
