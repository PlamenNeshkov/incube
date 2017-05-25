import os
from .common import Common
from configurations import values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Local(Common):

    SITE_ID = 1
    ALLOWED_HOSTS = ['*']

    CORS_ORIGIN_ALLOW_ALL = True

    DEBUG = values.BooleanValue(True)
    for config in Common.TEMPLATES:
        config['OPTIONS']['debug'] = DEBUG

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package={}'.format(BASE_DIR)
    ]

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
