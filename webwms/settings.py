"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.path
#os.environ['Path']='D:\\Develop\\Oracle11gx64\\instantclient_11_2;'+os.environ['Path']
os.environ['Path']='C:\\OracleClient\\Oleg\product\\11.2.0\\client_1\\BIN;'+os.environ['Path']
from django.core.urlresolvers import reverse_lazy

LOGIN_URL = '/wms/login/'
LOGIN_REDIRECT_URL = '/wms/main/'
#LOGIN_URL = reverse_lazy('/wms/login/')
#LOGIN_REDIRECT_URL = reverse_lazy('/wms/index/')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hpv!enzhq1ksfpmcjb2ev=0qrca2)fm!k*igz%&s56i#xo=jw('

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
    'wms',
    'googlecharts',
    'qsstats',
    'crispy_forms',
    'stickymessages',
    'datatableview',
    #'django_tables2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (

    'stickymessages.context_processors.latest_sticky_message',
    #'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TEMPLATE_DIRS = (
    './templates', # Change this to your own directory.
)

ROOT_URLCONF = 'webwms.urls'

WSGI_APPLICATION = 'webwms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# """
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'wmsdb11',
        'USER': 'web',
        'PASSWORD': 'oracle',
        'HOST': 'hercules.solvo.ru',
        'PORT': '1521',
    }
}

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

SOUTH_DATABASE_ADAPTERS = {
    'default': "south.db.oracle"
}