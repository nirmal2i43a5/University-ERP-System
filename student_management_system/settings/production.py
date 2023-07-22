# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

from .base import *


DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1",
"localhost",
'mis.iconichive.com',
'www.mis.iconichive.com'

]


DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }
