"""
Django settings for splatterpunk project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
VERSION = '0.1.0'

import os
from os.path import join, abspath, dirname, normpath
from django.core.exceptions import ImproperlyConfigured
import dj_database_url


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_message = "Set the {name} environment variable".format(
            name=var_name
        )
        raise ImproperlyConfigured(error_message)


# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)
def here(*x):
    return join(abspath(dirname(__file__)), *x)


def root(*x):
    return join(abspath(PROJECT_ROOT), *x)

PROJECT_ROOT = normpath(here("..", "..", ".."))
PROJECT_NAME = "splatterpunk"
SITE_NAME = "Splatterpunk"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

TEMPLATE_DIRS = (
    root(PROJECT_NAME, "templates"),
)

ALLOWED_HOSTS = [
    '{project}.herokuapp.com'.format(project=PROJECT_NAME),
    '{project}.herokuapp.com.'.format(project=PROJECT_NAME),
]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Kit', 'kit.la.t@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'south',
    'rest_framework',
    'pipeline',
)

LOCAL_APPS = (
    'sheets',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '{project}.urls'.format(project=PROJECT_NAME)

WSGI_APPLICATION = '{project}.wsgi.application'.format(project=PROJECT_NAME)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config(
    default='postgres://localhost/{project}'.format(project=PROJECT_NAME)
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(PROJECT_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/
#   #std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(PROJECT_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/
#   #staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = '{project}.custom_storages.S3PipelineStorage'.format(
    project=PROJECT_NAME
)

AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
ADMIN_MEDIA_PREFIX = S3_URL + 'admin/'

PIPELINE_CSS = {
    'all': {
        'source_filenames': (
            # 'css/bootstrap.css',
            # 'css/bootstrap-responsive.css',
            # 'css/project.css'
        ),
        'output_filename': 'css/all.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'all': {
        'source_filenames': (
            # 'js/jquery-1.9.1.js',
            # 'js/bootstrap.js',
            # 'js/project.js'
        ),
        'output_filename': 'js/all.js',
    }
}
########## END STATIC CONFIGURATION


# Tests
# Thorny!
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-yanc', '--stop', PROJECT_NAME]


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
########## END LOGGING CONFIGURATION
