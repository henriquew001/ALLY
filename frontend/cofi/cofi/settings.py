"""
Django settings for cofi project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable for secret key.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-*ryw^4*an$ffr*g9ig&=t9!)!fhg*zv31nms4(b5i6y)3@t7_m')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Better way to handle boolean

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')]


# Application definition

INSTALLED_APPS = [
    'home',
    'cofi',
    'accounts',
    'focoquiz',
    'about',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'cofi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"], # where to search for templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cofi.wsgi.application'


AUTH_USER_MODEL = 'accounts.CustomUser'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Construct the database URL dynamically
DB_ENGINE = os.environ.get("DB_ENGINE", "mysql")
DB_USER = os.environ.get("DB_USER", "app_user")  # Correct default user
DB_PASSWORD = os.environ.get("DB_PASSWORD", "testpw") # Use environment variable
DB_HOST = os.environ.get("DB_HOST", "db_dev")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_DATABASE", "conscious_fit_dev")

DB_TEST_NAME = os.environ.get("DB_TEST_DATABASE", "conscious_fit_testing")

if DB_ENGINE == "sqlite3":
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
else:  # Assume MySQL/MariaDB if not SQLite
     DATABASE_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL)
}

# Add OPTIONS *only* for MySQL.  Crucially important for character set.
if DB_ENGINE == "mysql":
    DATABASES["default"]["OPTIONS"] = {
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci',  # Or utf8mb4_0900_ai_ci
        'connect_timeout': 10,
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
    DATABASES["default"]["TEST"] = { # Added comma here!
        "NAME": DB_TEST_NAME
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
    ('pt-br', 'Spanish')
]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'