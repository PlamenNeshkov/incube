import os
from configurations import values
from boto.s3.connection import OrdinaryCallingFormat
from .common import Common

try:
    # Python 2.x
    import urlparse
except ImportError:
    # Python 3.x
    from urllib import parse as urlparse

class Production(Common):

    SITE_ID = 2
    ALLOWED_HOSTS = ['.incube.io']

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = values.SecretValue()

    INSTALLED_APPS += ("djangosecure", )

    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SESSION_COOKIE_SECURE = values.BooleanValue(False)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)

    INSTALLED_APPS += ("gunicorn", )

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    INSTALLED_APPS += ('storages',)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = values.Value('DJANGO_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = values.Value('DJANGO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = values.Value('DJANGO_AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = values.Value('public-read')
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False
    MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
    AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400, s-maxage=86400, must-revalidate',
    }

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '{}:{}'.format(redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'DB': 0,
                'PASSWORD': redis_url.password,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 50,
                    'timeout': 20,
                }
            }
        }
    }
