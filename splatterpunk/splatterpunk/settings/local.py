from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS += (
    'django_nose',
)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION
