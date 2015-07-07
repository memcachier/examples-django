# Django settings for MemCachier django example.
import os

## MemCachier Settings
## ===================
# Docs: http://sendapatch.se/projects/pylibmc/behaviors.html
#       http://docs.libmemcached.org/memcached_behavior.html
#       https://github.com/django-pylibmc/django-pylibmc
#       https://docs.djangoproject.com/en/1.6/topics/cache
if os.environ.get('DEVELOPMENT', None):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }
else:
    # Configure server credentials
    os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

    # Configure cache settings
    CACHES = {
        'default': {
            # Use pylibmc
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',

            # Use binary memcache protocol (needed for authentication)
            'BINARY': True,

            # TIMEOUT is not the connection timeout! It's the default expiration
            # timeout that should be applied to keys! Setting it to `None`
            # disables expiration.
            'TIMEOUT': None,

            'OPTIONS': {
                # Enable faster IO
                'no_block': True,
                'tcp_nodelay': True,

                # Keep connection alive
                'tcp_keepalive': True,

                # Timeout for set/get requests (sadly timeouts don't mark a
                # server as failed, so failover only works when the connection
                # is refused)
                '_poll_timeout': 2000,

                # Use consistent hashing for failover
                'ketama': True,

                # Configure failover timings
                'connect_timeout': 2000,
                'remove_failed': 4,
                'retry_timeout': 2,
                'dead_timeout': 10
            }
        }
    }

## ======================================================================
## EVERYTHING BELOW IS CONFIGURATION UNRELATED TO THIS MEMCACHIER EXAMPLE
## ======================================================================

## Database Settings (none)
## ========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

## Other Settings
## ==============
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    "static/"
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'l&amp;nd6u%i-s)2c)s5=^i2#v*4)%i9j-g^yo=)z#(#+5pe)o_=%v'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'memcachier_algebra.urls'

WSGI_APPLICATION = 'memcachier_algebra.wsgi.application'

TEMPLATE_DIRS = (
    "templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
