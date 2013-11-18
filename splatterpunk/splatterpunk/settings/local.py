from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'django_nose',
)

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION
