from confy import database, env
import os
import sys
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(Path(__file__).resolve().parents[1])
PROJECT_DIR = str(Path(__file__).resolve().parents[0])
# Add PROJECT_DIR to the system path.
sys.path.insert(0, PROJECT_DIR)

# Settings defined in environment variables.
DEBUG = env('DEBUG', False)
SECRET_KEY = env('SECRET_KEY', 'PlaceholderSecretKey')
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', False)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', False)
if not DEBUG:
    ALLOWED_HOSTS = env('ALLOWED_DOMAINS', '').split(',')
else:
    ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1', '::1']
ROOT_URLCONF = 'ibms_project.urls'
WSGI_APPLICATION = 'ibms_project.wsgi.application'
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'crispy_forms',
    'webtemplate_dbca',
    'ibms',
    'sfm',
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dpaw_utils.middleware.SSOLoginMiddleware',
]
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'ibms_project', 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',
                'ibms_project.context_processors.standard'
            ],
        },
    }
]
SITE_TITLE = 'Integrated Business Management System'
SITE_ACRONYM = 'IBMS'
APPLICATION_VERSION_NO = '2.4'
ADMINS = ('asi@dbca.wa.gov.au',)
MANAGERS = (
    ('Zen Wee', 'zen.wee@dbca.wa.gov.au', '9219 9928'),
    ('Neil Clancy', 'neil.clancy@dbca.wa.gov.au', '9219 9926'),
)
SITE_ID = 1
ANONYMOUS_USER_ID = 1
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
CONFLUENCE_URL = env('CONFLUENCE_URL', '')
# URLs to the IBM Code Updater spreadsheets on Confluence, so that the Custodian
# can update them without a code change.
IBM_CODE_UPDATER_URI = env('IBM_CODE_UPDATER_URI', '')
IBM_SERVICE_PRIORITY_URI = env('IBM_SERVICE_PRIORITY_URI', '')
IBM_RELOAD_URI = env('IBM_RELOAD_URI', '')
IBM_DATA_AMEND_URI = env('IBM_DATA_AMEND_URI', '')
HELP_URL = CONFLUENCE_URL
CRISPY_TEMPLATE_PACK = 'bootstrap3'
DATA_UPLOAD_MAX_NUMBER_FIELDS = None  # Required to allow end-of-month GLPivot bulk deletes.


# Database configuration
DATABASES = {
    # Defined in DATABASE_URL env variable.
    'default': database.config(),
}


# Static files (CSS, JavaScript, Images)
# Ensure that the media directory exists:
if not os.path.exists(os.path.join(BASE_DIR, 'media')):
    os.mkdir(os.path.join(BASE_DIR, 'media'))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'), )


# Internationalisation.
USE_I18N = False
USE_TZ = True
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
DATE_INPUT_FORMATS = (
    '%d/%m/%y',
    '%d/%m/%Y',
    '%d-%m-%y',
    '%d-%m-%Y',
    '%d %b %Y',
    '%d %b, %Y',
    '%d %B %Y',
    '%d %B, %Y')
DATETIME_INPUT_FORMATS = (
    '%d/%m/%y %H:%M',
    '%d/%m/%Y %H:%M',
    '%d-%m-%y %H:%M',
    '%d-%m-%Y %H:%M',)


# Email settings.
EMAIL_HOST = env('EMAIL_HOST', 'email.host')
EMAIL_PORT = env('EMAIL_PORT', 25)


# Logging settings - log to stdout/stderr
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {'format': '%(name)-12s %(message)s'},
        'verbose': {'format': '%(asctime)s %(levelname)-8s %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
		'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
			'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
			'propagate': False,
        },
        'ibms': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    }
}


# Sentry configuration
if env('RAVEN_DSN', False):
    RAVEN_CONFIG = {'dsn': env('RAVEN_DSN')}
