from .base import *

INSTALLED_APPS += (
    'django_nose',
)

DATABASES['default'] = dj_database_url.config(
    default='postgres://postgres@localhost/{project}'.format(
        project=PROJECT_NAME
    )
)
