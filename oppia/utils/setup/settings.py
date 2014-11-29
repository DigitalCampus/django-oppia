"""
Django settings for oppia_core project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'django-<PROJ_NAME>-oppia'))
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(53vx$08wtw3y*6e9!$ggorl23f@4)3it8*eq78y3l5rfc=lte'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'tastypie',
    'oppia', 
    'oppia.quiz',
    'oppia.profile',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'oppia_<PROJ_NAME>.urls'

WSGI_APPLICATION = 'oppia_<PROJ_NAME>.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'oppia_<PROJ_NAME>',                      # Or path to database file if using sqlite3.
        'USER': '<PROJ_NAME>',                      # Not used with sqlite3.
        'PASSWORD': 'admin<PROJ_NAME>',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = '<DEV_ROOT>/oppia_<PROJ_NAME>/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '<DEV_ROOT>/oppia_<PROJ_NAME>/static/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Specify languages available
gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
)

from oppia import local_settings
local_settings.modify(globals())

# OppiaMobile settings
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/profile/login/'
SERVER_EMAIL = 'alex@digital-campus.org'
COURSE_UPLOAD_DIR = '<DEV_ROOT>/oppia_<PROJ_NAME>/upload/'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/alex/temp/'

