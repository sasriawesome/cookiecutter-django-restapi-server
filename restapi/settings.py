"""
Django settings for {{cookiecutter.project_name}} project.
"""
import os
import inspect
import datetime
import pydf
from restapi import __version__ as version


# =============================================================================
# SECURITY WARNING: 
# Don't run with debug turned on in production!
# =============================================================================

DEBUG = bool(os.getenv('DEBUG', True))

# Build paths
PROJECT_NAME = 'SISTER'
PROJECT_VERSION = version
PROJECT_DESCRIPTION = """
    Django REST API boiler plate project template.
    Speed your API Developmet
"""
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SITE_ID = os.getenv('SITE_ID', int(1))

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

SECRET_KEY = os.getenv('SECRET_KEY', 'important-secret-key')

ALLOWED_HOSTS = ['*']

# =============================================================================
# Application definition
# =============================================================================

PRODUCTION_APPS = [
    
    'restapi.core',
    'restapi.auth',
    'restapi.admin',
    'restapi.api',
    'restapi.modules.todo',

    'constance',
    'drf_yasg',
    'djoser',
    'rest_framework',

    "django_rq",
    'django_filters',

    # Admin stuffs
    'rangefilter',  # https://github.com/silentsokolov/django-admin-rangefilter
    'admin_numeric_filter',  # https://pypi.org/project/django-admin-numeric-filter/
    'django.contrib.admin',
    'django.contrib.messages',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

DEVELOPMENT_APPS = [
    # Include only when DEBUG=True
]

if DEBUG:
    INSTALLED_APPS = PRODUCTION_APPS + DEVELOPMENT_APPS
else:
    INSTALLED_APPS = PRODUCTION_APPS

WSGI_APPLICATION = 'restapi.wsgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'restapi.core.context_processors.settings',
            ],
        },
    },
]

# =============================================================================
# Database
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# If using heroku
# DATABASES['default'].update(
#    dj_database_url.config(conn_max_age=500, ssl_require=True)
# )

# =============================================================================
# Authentications
# =============================================================================

AUTH_USER_MODEL = 'restapi_auth.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework_simplejwt.authentication.JWTAuthentication'
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =============================================================================
# Internationalization
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

FORMAT_MODULE_PATH = [
    'restapi.formats',
]

# =============================================================================
# Static files (CSS, JavaScript, Images)
# =============================================================================

# Using AWS Bucket or Digital Ocean Space

# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'storagename')
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'accesskeyid')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'secretaccesskey')
# AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', 'cdn.amazonaws.com')
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'


# =============================================================================
# Email Backend
# =============================================================================

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'restapi.noreply@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_USER', 'somepassword')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# =============================================================================
# REST FRAMEWORK
# =============================================================================

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'restapi.api.schemas.ReadWriteAutoSchema'
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# =============================================================================
# Redis Cache
# =============================================================================

CACHE_TTL = 60 * 5

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # the password you should use to connect Redis is not URL-safe
            # "PASSWORD": "mysecret"
        },
        "KEY_PREFIX": os.getenv('SITE_NAME', 'restapi')
    },
}

# =============================================================================
# Redis Queues
# =============================================================================

RQ_QUEUES = {
    'default': {
        'DEFAULT_TIMEOUT': 180,
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379/1'), # If you're on Heroku
    },
    'high': {
        'DEFAULT_TIMEOUT': 360,
        # 'PASSWORD': 'some-password',
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    },
    'low': {
        'DEFAULT_TIMEOUT': 500,
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    }
}


# =============================================================================
# Django WKHTMLTOPDF and PYDF
# =============================================================================

pydf_path = os.path.dirname(inspect.getfile(pydf))
wkhtml_executable = os.path.join(pydf_path, 'bin','wkhtmltopdf.exe')
WKHTMLTOPDF_PATH = wkhtml_executable.replace('\\','/')

WKHTMLTOPDF_CMD = os.getenv('WKHTMLTOPDF_CMD', WKHTMLTOPDF_PATH)


# Optional 
# WKHTMLTOPDF_CMD_OPTIONS = {
#     'quiet': False,
# }

# =============================================================================
# Constance Settings
# =============================================================================

CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

CONSTANCE_REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 3,
}

CONSTANCE_ADDITIONAL_FIELDS = {
    'char_field': ['django.forms.CharField', {}],
    'date_field': ['django.forms.DateField', {
        'widget': 'django.contrib.admin.widgets.AdminDateWidget'
    }],
    'image_field': ['django.forms.ImageField', {}],
    'email_field': ['django.forms.EmailField', {}]
}

CONSTANCE_CONFIG = {
    # Website Settings
    'SITE_LOGO': ('logo.png', 'Website Logo', 'image_field'),
    'SITE_TITLE': ('My Website', 'Website title', 'char_field'),
    'SITE_SUBTITLE': ('Another Awesome Website', 'Website subtitle', 'char_field'),
    'SITE_DESCRIPTION': ('Website about good service', 'Website description'),
    # Company Profile
    'COMPANY_NAME': (
        'My Company',
        'Company or commercial name',
        'char_field'
        ),
    'COMPANY_ADDRESS': (
        'Jl. Ikan Sebelah No.8, Kec. Pesawahan',
        'Company address, street name etc.'
        ),
    'COMPANY_CITY': ('Bandar Lampung', '', 'char_field'),
    'COMPANY_PROVINCE': ('Lampung', '', 'char_field'),
    'COMPANY_COUNTRY': ('Indonesia', '', 'char_field'),
    'COMPANY_POSTALCODE': ('35223', '', 'char_field'),
    'COMPANY_PHONE': ('0721373767', 'Valid phone number', 'char_field'),
    'COMPANY_EMAIL': ('mycompany@gmail.com', 'Company email address', 'email_field'),
    # Tahun Anggaran
    'FISCAL_DATE_START': (datetime.date(2020, 1, 1), 'Fiscal start date', 'date_field'),
    'FISCAL_DATE_END': (datetime.date(2020, 12, 31), 'Fiscal start date', 'date_field'),
    # PDF Settings
    'PDF_MARGIN_TOP': (40, ''),
    'PDF_MARGIN_LEFT': (30, ''),
    'PDF_MARGIN_RIGHT': (30, ''),
    'PDF_MARGIN_BOTTOM': (30, ''),
    'PDF_ORIENTATION': ('portrait', 'Page orientation')
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General Settings': (
        'SITE_LOGO', 
        'SITE_TITLE', 
        'SITE_SUBTITLE',
        'SITE_DESCRIPTION'
    ),
    'Company Settings': (
        'COMPANY_NAME',
        'COMPANY_ADDRESS',
        'COMPANY_CITY',
        'COMPANY_PROVINCE',
        'COMPANY_POSTALCODE',
        'COMPANY_PHONE',
        'COMPANY_EMAIL',
    ),
    'Reports Settings': (
        'FISCAL_DATE_START',
        'FISCAL_DATE_END',
        'PDF_MARGIN_TOP',
        'PDF_MARGIN_LEFT',
        'PDF_MARGIN_RIGHT',
        'PDF_MARGIN_BOTTOM',
        'PDF_ORIENTATION'
    ),
}

# If you need custom exception handlers
# RQ_EXCEPTION_HANDLERS = ['path.to.my.handler']

# =============================================================================
# Heroku Setup
# =============================================================================

# django_heroku.settings(locals())

# try:
#     from .local import *
# except ImportError:
#     pass
