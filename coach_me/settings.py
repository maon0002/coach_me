import os
# from os import path
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)me+gt_-s)5ga$x9j07u1$nya12k(mzka+&cb&svui2jx7ysq&'
# SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# DEBUG = FALSE // plus do 404 page
DEBUG = bool(int(os.environ.get('DEBUG')))


ALLOWED_HOSTS = []

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ') #'for_deploy qa.for_deploy'
# ALLOWED_HOSTS = (
#     '127.0.0.1:8000',
# )


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# C:\Users\LENOVO\PycharmProjects\coach_me\db.sqlite3_bckp
# jdbc:sqlite:C:\Users\LENOVO\PycharmProjects\coach_me\db.sqlite3_bckp

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3_0',
#         # 'NAME': BASE_DIR / 'db.sqlite3_2',
#     }
# }
#
DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),

    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": os.getenv('DB_HOST', 'localhost'),
#         "PORT": os.getenv('DB_PORT', '5432'),
#         "NAME": os.getenv('DB_NAME', 'coachme_db'),
#         "USER": os.getenv('DB_USER', 'maon0002'),
#         "PASSWORD": os.getenv('DB_PASSWORD', 'nirvana'),
#     }
# }

#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "fruitipedia_db", # TODO db
#         "USER": "maon0002",
#         "PASSWORD": "nirvana",
#         "HOST": "127.0.0.1",
#         "PORT": "5432",
#     }
# }


# Application definition
MY_APPS = [
    # 'coach_me.accounts',
    'coach_me.accounts.apps.AccountsConfig',
    'coach_me.bookings',
    'coach_me.profiles',
    'coach_me.lectors',
    'coach_me.trainings',
]

INSTALLED_APPS = [
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',

                     'widget_tweaks',

                 ] + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coach_me.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'coach_me.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'application_cache',
    }
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

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)
# STATIC_ROOT = os.environ.get('STATIC_ROOT', BASE_DIR / 'static')

MEDIA_URL = '/media/'
# MEDIA_ROOT = path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Default URL to redirect to **after successful login**
LOGIN_REDIRECT_URL = reverse_lazy('index')

# Default URL to redirect to **after successful logout**
LOGOUT_REDIRECT_URL = reverse_lazy('index')

# Default URL to redirect to for **login**
LOGIN_URL = reverse_lazy('login_user')

# Defines the model for **Users**
# AUTH_USER_MODEL = 'accounts.BookingUser'
AUTH_USER_MODEL = 'accounts.BookingUser'

#SMTP config
# SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
#
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
# EMAIL_HOST_PASSWORD = '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' #SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True




#
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
# EMAIL_HOST_PASSWORD = 'jpisehhqplalzlkr'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

EMAIL_USE_TLS = True
# EMAIL_USE_TLS = bool(int(os.getenv('EMAIL_USE_TLS')))
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'coachme.demoapp@gmail.com'
EMAIL_HOST_PASSWORD = 'jpisehhqplalzlkr'