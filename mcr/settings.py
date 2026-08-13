from pathlib import Path
from django.contrib import messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-69!s0^#3v8m5mn(0h#3e&$9tkoq2s*a1rj&ix*n9f3egjj^6e%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mcroesperanza.local','localhost','127.0.0.1','192.168.100.44']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usr',
    'django.contrib.humanize',
    'birth',
    'marriage',
    'death',
    'django_bootstrap5',
    'bootstrap5',
    'import_export',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mcr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db/db.sqlite3',
    # }
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'mcroesperanza',
        'HOST': 'localhost',         # Use 'localhost' or your server IP
        'PORT': '5432',              # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS=[BASE_DIR/'static']
MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL='/'
LOGOUT_REDIRECT_URL = 'login'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
BS_ICONS_CUSTOM_PATH = 'icons/'
MESSAGE_TAGS={
    messages.ERROR:'danger',
    messages.SUCCESS:'success',
}
WKHTMLTOPDF_CMD =os.path.join(STATIC_URL,'wkhtmltopdf.exe')
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_ENCODING = 'utf-8-sig'
CSRF_TRUSTED_ORIGINS=['http://192.168.100.44:8000',
                      'http://192.168.100.44',
                      'http://mcroesperanza.local:8000',
                      'http://mcroesperanza.local'
                      'http://localhost:8000']
SESSION_COOKIE_AGE=600
SESSION_SAVE_EVERY_REQUEST=True
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
DATA_UPLOAD_MAX_NUMBER_FILES=1000
