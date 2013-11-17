"""
Django settings for splatterpunk project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
VERSION = '0.1.0'

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
import os


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
from os.path import join, abspath, dirname


def here(*x):
    return join(abspath(dirname(__file__)), *x)


def root(*x):
    return join(abspath(PROJECT_ROOT), *x)

PROJECT_ROOT = here("..", "..", "..")
PROJECT_NAME = "splatterpunk"
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

ALLOWED_HOSTS = []


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
    'django_nose',
    'rest_framework',
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
    default='postgres://localhost/splatterpunk'
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


# Tests
# Thorny!
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-yanc', '--stop', PROJECT_NAME]
