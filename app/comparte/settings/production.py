# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": os.environ.get("DB_HOST"),
#         "NAME": os.environ.get("DB_NAME"),
#         "USER": os.environ.get("DB_USER"),
#         "PASSWORD": os.environ.get("DB_PASS"),
#     }
# }

from .base import *

DEBUG = False
ALLOWED_HOSTS.extend(filter(None, os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")))

# Use PostgreSQL for production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}

STATIC_URL = "/static/static/"
MEDIA_URL = "/static/media/"
MEDIA_ROOT = "/vol/web/media"
STATIC_ROOT = "/vol/web/static"

# CORS_ALLOWED_ORIGINS = []
# CORS_ALLOWED_ORIGINS.extend(
#     filter(None, os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").split(","))
# )
