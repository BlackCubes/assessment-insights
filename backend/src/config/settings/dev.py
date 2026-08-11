from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vop!er052386dt%wjitvr-h8-0_(+md+6e#+17pqw^gdwb@h%j"

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_METHODS = [
    "GET",
]

try:
    from .local import *
except ImportError:
    pass
