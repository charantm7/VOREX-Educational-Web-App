"""
Django settings for studyroom project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cox_a!8#h^j(w*4g-n^3#9^-55vbv+il0--mfr*7=v675wlxbm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['vorexhub.onrender.com', 'localhost', '127.0.0.1', 'www.vorexhub.xyz']


CSRF_TRUSTED_ORIGINS = [
    'https://vorexhub.onrender.com',
    'https://www.vorexhub.xyz',
]

# Application definition
SITE_ID = 4

INSTALLED_APPS = [
    
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'base',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',   
    'allauth.socialaccount.providers.google',
    'django.contrib.humanize',
    'django_select2',
    'django.contrib.staticfiles',
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,  
    }
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'studyroom.urls'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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
ASGI_APPLICATION = 'studyroom.asgi.application'
WSGI_APPLICATION = 'studyroom.wsgi.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vorexdb',
        'USER': 'vorex',
        'PASSWORD': 'rlZsgwy9gSURb4Sj6hk6vemPgxuwTpXB',
        'HOST': 'dpg-d089vongi27c738bf6u0-a',  # e.g., "dpg-d089vongi27c738bf6u0-a"
        'PORT': '5432',  # Default PostgreSQL port
    }
}

DATABASES['default'] = dj_database_url.parse("postgresql://vorexhub_user:kcpmQ5tkaRZ7t0ptfzqI1wPrheqaR2DG@dpg-d0stumali9vc73dd0dj0-a.oregon-postgres.render.com/vorexhub")


#postgresql://vorex:rlZsgwy9gSURb4Sj6hk6vemPgxuwTpXB@dpg-d089vongi27c738bf6u0-a.oregon-postgres.render.com/vorexdb

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

STATICFILES_DIRS = [
    (BASE_DIR/'static')
]

STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

# Redirect URLs after login and logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_USERNAME_GENERATOR = lambda user: user.email.split('@')[0]
ACCOUNT_SIGNUP_FIELDS = ['email', 'password1', 'password2']  


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Media URL configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vorexx07@gmail.com'
EMAIL_HOST_PASSWORD = 'ufhtzvedowwsvaew'
DEFAULT_FROM_EMAIL = 'Vorex Support <vorexx07@gmail.com>'


SELECT2_CACHE_BACKEND = 'default'


