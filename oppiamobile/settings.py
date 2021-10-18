"""
Django settings for OppiaMobile project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uzekt30thl4&hw)p@c#ht=b8mn!3l080kmnuk7ez+g5l%lb*p9'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

ALLOWED_HOSTS = []
DEBUG = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oppia.middleware.LoginRequiredMiddleware',

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.i18n',
                'oppia.context_processors.get_points',
                'oppia.context_processors.get_version',
                'oppia.context_processors.get_settings',
                'oppia.context_processors.add_dashboard_access_log'
            ],
            'debug': True,
        },
    },
]

INSTALLED_APPS = [
    'quiz',
    'profile',
    'content',
    'av',
    'settings',
    'summary',
    'reports',
    'activitylog',
    'viz',
    'gamification',
    'oppia',
    'tastypie',
    'helpers',
    'integrations',
    'serverregistration',
    'crispy_forms',
    'sass_processor',
    'sorl.thumbnail',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

TIME_ZONE = 'UTC'
USE_TZ = True
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

ROOT_URLCONF = 'oppiamobile.urls'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/'
SERVER_EMAIL = 'adming@email.org'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-GB'
USE_I18N = True
USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "oppia", "locale")
]

LANGUAGES = ('en', _('English'))

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Login and logout settings
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-redirect-url
LOGIN_URL = '/profile/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Exempt URLs (used by LoginRequiredMiddleware)
LOGIN_EXEMPT_URLS = (
    r'^server/$',
    r'^profile/login/$',
    r'^profile/register/',
    r'^profile/reset/',
    r'^profile/setlang/$',
    r'^profile/delete/complete/$',
    r'^$',
    r'^about/$',
    r'^terms/$',
    r'^api/',  # allow any URL under api/* - auth handled by api_key
    r'^modules/api/',  # allow any URL under modules/api/* - auth by api_key
    r'^badges/api/',  # allow any URL under badges/api/* - auth by api_key
    r'^content/video-embed-helper/$',
    r'^content/media-embed-helper/$',
    r'^media/temp/',
    r'^media/uploaded/',
    r'^api/activitylog/',
    r'^view/$',
    r'^accounts/password_reset/',
    r'^accounts/reset/',
    r'^certificate/validate/'
)

# OppiaMobile Settings
COURSE_UPLOAD_DIR = os.path.join(ROOT_DIR, 'upload')

OPPIA_METADATA = {
    'NETWORK': False,
    'DEVICE_ID': False,
    'SIM_SERIAL': False,
    'WIFI_ON': True,
    'NETWORK_CONNECTED': True,
    'BATTERY_LEVEL': False,
}

# turns on/off ability for users to self register
OPPIA_ALLOW_SELF_REGISTRATION = True
OPPIA_ALLOW_PROFILE_EDITING = True
OPPIA_SHOW_GRAVATARS = True

# determines if the points system is enabled
OPPIA_POINTS_ENABLED = True

# determines if the badges system is enabled
OPPIA_BADGES_ENABLED = True

BADGE_AWARDING_METHOD = 'all_activities'

OPPIA_GOOGLE_ANALYTICS_ENABLED = False
OPPIA_GOOGLE_ANALYTICS_CODE = 'YOUR_GOOGLE_ANALYTICS_CODE'
OPPIA_GOOGLE_ANALYTICS_DOMAIN = 'YOUR_DOMAIN'

OPPIA_MAX_UPLOAD_SIZE = 5242880  # max course file upload size - in bytes

OPPIA_VIDEO_FILE_TYPES = ("video/m4v", "video/mp4", "video/3gp", "video/3gpp")
OPPIA_AUDIO_FILE_TYPES = ("audio/mpeg", "audio/amr", "audio/mp3")
OPPIA_MEDIA_FILE_TYPES = OPPIA_VIDEO_FILE_TYPES + OPPIA_AUDIO_FILE_TYPES

OPPIA_UPLOAD_TRACKER_FILE_TYPES = [("application/json")]

# Android app PackageId - for Google Play link and opening activities
# from digest
OPPIA_ANDROID_DEFAULT_PACKAGEID = 'org.digitalcampus.mobile.learning'
OPPIA_ANDROID_PACKAGEID = 'org.digitalcampus.mobile.learning'

# if the app is not on Google Play, we rely on the core version for store
# links
OPPIA_ANDROID_ON_GOOGLE_PLAY = True

API_LIMIT_PER_PAGE = 0

MEDIA_PROCESSOR_PROGRAM = "ffprobe"
MEDIA_PROCESSOR_PROGRAM_PARAMS = ""

# Database - mainly this is for the automated testing
# a proper RDBMS should be configured in your settings_secret.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

# Import secret_settings.py (if exists)
# > see settings_secret.py.template for reference
try:
    from oppiamobile.settings_secret import *
except ImportError:
    print("settings_secret.py file could not be found.")
