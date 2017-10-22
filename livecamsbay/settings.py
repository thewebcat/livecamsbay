"""
Django settings for livecamsbay project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import djcelery
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w_vyy4m%hpkz*r3ou45so&gu%c53&lvs0fjclx=hliiw3r@t04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1', '::1']

# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    #'djadmin',
    #'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # pip apps
    'modeltranslation',
    'django_filters',
    'sorl.thumbnail',
    'spurl',
    'debug_toolbar',
    'bootstrap3',
    'sekizai',
    'easy_thumbnails',
    'cities_light',
    'ckeditor',
    'widget_tweaks',
    'nocaptcha_recaptcha',
    'djcelery',

    # my apps
    'main',
    'seo',
    'call_orders',
    'authorization',
    'accounts',
    'newsletter_email',
    'email_sender',
    'private_messages',
    'tickets',
    'news',
    'tags',
    'feedback',
    'cms',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

SITE_ID = 1

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ru',]
CITIES_LIGHT_INCLUDE_COUNTRIES = ['RU']

NORECAPTCHA_SITE_KEY = '6LeVAiMTAAAAAPZSltV-WfpDwqyphmxsIU_U6gsF'
NORECAPTCHA_SECRET_KEY = '6LeVAiMTAAAAAIoGXD8MP6qFEKDMZzgtJ6o0fLn8'

ADMIN_TOOLS_INDEX_DASHBOARD = 'livecamsbay.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'livecamsbay.dashboard.CustomAppIndexDashboard'

MIDDLEWARE_CLASSES = [
    'livecamsbay.middleware.CurrentUser',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livecamsbay.middleware.QuickPanel',
    'seo.middleware.RuleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'livecamsbay.urls'

AUTHENTICATION_BACKENDS = (
    'main.authbackend.AuthBackend',
    'main.authbackend.OneTimeAccess',
    'main.authbackend.EmailAccess',
)

AUTH_USER_MODEL = 'main.User'

LOGIN_URL = reverse_lazy('authorization:enter')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        #'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.core.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #
                'livecamsbay.context_processors.get_settings',
                'livecamsbay.context_processors.get_cam_services',

                #
                'sekizai.context_processors.sekizai',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'livecamsbay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'livecamsbay.translation'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

COMPANY = "Amigo Stone"
DOMAIN = ""
ADMIN_EMAIL = 'beholdthegreatnessofpotato@gmail.com'
ADMIN_EMAILS = {
    'info': 'info@livecamsbay.com',
    'editor': 'editor@livecamsbay.com',
    'manager': 'manager@livecamsbay.com',
    'support': 'support@livecamsbay.com',
    'advert': 'advert@livecamsbay.com',
    'robot': 'noreply@livecamsbay.com',
    'main': 'beholdthegreatnessofpotato@gmail.com'
}

# Size all imgs
IMG_SIZE = {
    'S': (),
    'M': (),
    'L': (250, 250),
    'original': (350, 350)
}

PREVIEW_THUMBNAIL_OPTIONS = {'size': (130, 100), 'crop': True}

def preview_default_image():
    from easy_thumbnails.files import get_thumbnailer
    return get_thumbnailer(open(DEFAULT_IMAGE), relative_name='default.png')\
        .get_thumbnail(PREVIEW_THUMBNAIL_OPTIONS).url

FILE_MIME_TYPE = {
    'image/jpeg': None, 'image/png': None, 'application/pdf': preview_default_image, 'image/tiff': None,
    'application/octet-stream': preview_default_image, 'application/dxf': preview_default_image,
    'drawing/x-dwf': preview_default_image, 'model/vnd.dwf': preview_default_image,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': preview_default_image,
    'application/msword': preview_default_image,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': preview_default_image,
    'application/vnd.ms-excel': preview_default_image
}

IMAGE_EXTENTION = {
    'jpg': FILE_MIME_TYPE['image/jpeg'],
    'jpeg': FILE_MIME_TYPE['image/jpeg'],
    'png': FILE_MIME_TYPE['image/png'],
    'tiff': FILE_MIME_TYPE['image/tiff'],
}

FILE_EXTENTION = {
    'pdf': FILE_MIME_TYPE['application/pdf'],
    'dws': FILE_MIME_TYPE['application/octet-stream'],
    'dwt': FILE_MIME_TYPE['application/dxf'],
    'dxf': FILE_MIME_TYPE['drawing/x-dwf'],
    'dwf': FILE_MIME_TYPE['model/vnd.dwf'],
    'docx': FILE_MIME_TYPE['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    'doc': FILE_MIME_TYPE['application/msword'],
    'xlsx': FILE_MIME_TYPE['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
    'xls': FILE_MIME_TYPE['application/vnd.ms-excel']
}

DEFAULT_IMAGE = os.path.join(PROJECT_DIR, 'main/static', 'images/default.png')

#############################
djcelery.setup_loader()

# BROKER_URL = 'redis+socket:///var/run/redis/redis.sock'
# CELERY_RESULT_BACKEND = 'redis+socket:///var/run/redis/redis.sock'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 7 * 86400  # 7 days
CELERY_SEND_EVENTS = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

try:
    from local_settings import *
except ImportError:
    pass