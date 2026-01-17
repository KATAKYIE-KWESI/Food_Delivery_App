"""
Django settings for Food project.
"""

import os
from pathlib import Path
import dj_database_url
from decouple import config

# --------------------------
# Base directory
# --------------------------
# Fix: BASE_DIR points to Food/ folder, one level above settings.py
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# Security
# --------------------------
SECRET_KEY = config('SECRET_KEY')

# Turn off DEBUG in production
DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    'https://postarytenoid-panickingly-marline.ngrok-free.dev',
]

ALLOWED_HOSTS =  ['localhost', '127.0.0.1', '172.20.10.13','postarytenoid-panickingly-marline.ngrok-free.dev']

# --------------------------
# Installed Apps
# --------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Jolly.apps.JollyConfig',  # Your app
    'django.contrib.sites', # Required for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google'
]

SITE_ID = 1


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --------------------------
# Middleware
# --------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files on production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Jolly.middleware.CyberSecurityMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# --------------------------
# URL Configuration
# --------------------------
ROOT_URLCONF = 'Food.urls'

# --------------------------
# Templates
# --------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Global templates folder
        'DIRS': [BASE_DIR.parent / 'templates'],
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

# --------------------------
# WSGI
# --------------------------
WSGI_APPLICATION = 'Food.wsgi.application'

# Trust the ngrok origin for CSRF (Critical for mobile login/cart)
CSRF_TRUSTED_ORIGINS = [
    'https://postarytenoid-panickingly-marline.ngrok-free.dev'
]


# --------------------------
# Databases
# --------------------------
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# --------------------------
# Password Validators
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --------------------------
# Internationalization
# --------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------------
# Static files (CSS, JS, Images)
# --------------------------
STATIC_URL = '/static/'

# Location of global static files (ResturantApp/static/)
STATICFILES_DIRS = [
    BASE_DIR.parent / 'static'
]

# Where collectstatic will put files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage for compression & caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------
# Email Configuration (Brevo/Sendinblue)
# --------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = "KatCompany <kwabby950@gmail.com>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# paystack config
PAYSTACK_PUBLIC_KEY = "pk_test_1379197c153b84ae1fccf5a41f88f7cc131337d2"
PAYSTACK_SECRET_KEY = "sk_test_4c1fd9c08a5cfd4fd7b48e5fff358554baa264c3"

#Hugging face config
import os
HF_TOKEN = config("HF_TOKEN", default=None)

# Groq API
GROQ_API_KEY = config("GROQ_API_KEY")

#Telegram alerts
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')

#Forcing mobile to accept cookies
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

# Where to send users after they log in
LOGIN_REDIRECT_URL = '/'

# Where to send users after they log out
LOGOUT_REDIRECT_URL = '/'