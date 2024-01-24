from pathlib import Path
import os
import environ
#from google.oauth2 import service_account
#import dj_database_url
env = environ.Env()
environ.Env.read_env()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
ENVIRONMENT = env
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=os.environ.get('SECRET_KEY')
#SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = False    #'RENDER' not in os.environ

ALLOWED_HOSTS = ['*']

#RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
#if RENDER_EXTERNAL_HOSTNAME:
#    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INTERNAL_IPS = ['127.0.0.1']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
   'apps.graph',
   'apps.users',
   'apps.dashboards',
]

THIRD_PARTY_APPS = [
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'dpd_static_support',
    'channels',
    'channels_redis',
    'crum',
    #'debug_toolbar'
    #'dash_ag_grid'
    


]


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE= [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #"django.middleware.cache.UpdateCacheMiddleware",
    #"django.middleware.cache.FetchFromCacheMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    #me
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    #'crum.CurrentRequestUserMiddleware'
    'crum.CurrentRequestUserMiddleware',
    ##
   # 'debug_toolbar.middleware.DebugToolbarMiddleware'


]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION='core.routing.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'config_dashboard',
        'USER':'user_dashboard',
        'PASSWORD':'AVNS_qzIvl--8EycKmegEnCk',
        'HOST': 'db-mysql-prod-nisira-001-do-user-8636826-0.b.db.ondigitalocean.com',
        'PORT':'25060'
    }
    
    
}

DATABASES["default"]["ATOMIC_REQUESTS"] = False
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join (BASE_DIR, 'static')

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'core/static')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'#CompressedManifestStaticFilesStorage


#if not DEBUG:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    #STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

X_FRAME_OPTIONS = 'SAMEORIGIN'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND':'channels_redis.core.RedisChannelLayer',# 'channels.layers.InMemoryChannelLayer'
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379),],
            
        }
    }
}
ASGI_THREADS = 1000

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

PLOTLY_COMPONENTS = [
    'dash_mantine_components',
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components',
    'dpd_static_support',
    'dash_bootstrap_components',
    'dash_bootstrap_templates',
]


LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL='/user/login/'



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 16,
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

FILE_UPLOAD_PERMISSIONS = 0o640

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
#BROKER_CONNECTION_RETRY = True
#BROKER_CONNECTION_MAX_RETRIES = 0
#BROKER_CONNECTION_TIMEOUT = 120
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
"""
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
"""
"""
PLOTLY_DASH = {

    
    # Route used for the message pipe websocket connection
    "ws_route" :   "ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
    "insert_demo_migrations" : True,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,<
    "stateless_loader" : "demo.scaffold.stateless_app_loader",
}
"""
DATA_UPLOAD_MAX_MEMORY_SIZE=1000000000
MAX_ACTIVE_TASKS  = 100
#GOOGLE_APPLICATION_CREDENTIALS = 'apps/users/key/stable-hologram-410021-93f04a1d61d1.json'
#GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
#DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
#GS_BUCKET_NAME = 'bucket_nisira'
#STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'