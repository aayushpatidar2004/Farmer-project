import os
from pathlib import Path

import pymysql
pymysql.install_as_MySQLdb()

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
DEBUG = os.environ.get('DEBUG', 'True').lower() in {'1', 'true', 'yes', 'on'}
allowed_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver,0.0.0.0')
if allowed_hosts == '*':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [host.strip().strip("[]'\"") for host in allowed_hosts.split(',') if host.strip()]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        'CSRF_TRUSTED_ORIGINS',
        'https://*.onrender.com,https://localhost,https://127.0.0.1'
    ).split(',')
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    # Local apps
    'config',
    'accounts',
    'crops',
    'weather',
    'soil',
    'recommendations',
    'diseases',
    'market',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.EnsureFarmerProfileMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_admin_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration: prefer SQLite for local work unless MySQL is explicitly requested.
DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')
DB_NAME = os.environ.get('DB_NAME', 'db.sqlite3')

if DB_ENGINE in {'sqlite3', 'django.db.backends.sqlite3'}:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / DB_NAME,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'smart_farmer_db'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# Try connecting to database on startup check; if MySQL fails, fallback to sqlite3 in dev
try:
    if DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
        connection_params = {
            'host': DATABASES['default']['HOST'],
            'user': DATABASES['default']['USER'],
            'password': DATABASES['default']['PASSWORD'],
            'port': int(DATABASES['default']['PORT']),
            'connect_timeout': 2,
        }
        test_conn = pymysql.connect(**connection_params)
        test_conn.close()
except Exception:
    # If MySQL connection fails (e.g. MySQL service not running locally), fallback to SQLite for local development & testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in {'1', 'true', 'yes', 'on'}
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'noreply@smartfarmer.local')

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGOUT_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']
