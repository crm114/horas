import os

from configurations import Configuration, values


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    ENVIRONMENT = values.Value(environ_prefix=None, default='development')

    APPNAME = 'horas'

    DEBUG = False

    TEMPLATE_DEBUG = DEBUG

    SECRET_KEY = values.SecretValue(environ_prefix=None)
    SSO_SECRET_KEY = values.SecretValue(environ_prefix=None)

    DISCOURSE_SSO_REDIRECT_URL = 'http://comunidad.1hora.org/session/sso_login?'

    ALLOWED_HOSTS = ['localhost', 'unahora.herokuapp.com', '1hora.org']

    SITE_ID = 1

    DATE_FORMAT = 'D, F j, Y'

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # Third-party
        'south',
        'django_extensions',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.twitter',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.persona',
        'taggit',
        'notification',
        'gunicorn',
        'storages',
        'collectfast',
        'djangosecure',
        'bootstrap3',
        'markdown_deux',

        # Local apps
        'apps.core',
        'apps.profiles',
        'apps.search',
        'apps.meetings',
        'apps.stats',
        'apps.sso',
        'apps.comments',
    )

    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'apps.core.middleware.TimezoneMiddleware',
        'apps.core.middleware.EnsureCompleteProfileMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',

        'allauth.account.context_processors.account',
        'allauth.socialaccount.context_processors.socialaccount',
    )

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend'
    )

    # Custom user model
    AUTH_USER_MODEL = 'profiles.User'
    LOGIN_URL = '/accounts/login/'

    # allauth settings
    ACCOUNT_ADAPTER = 'apps.profiles.adapters.AccountAdapter'
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
    ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Horas] '
    ACCOUNT_LOGOUT_ON_GET = True
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
    ACCOUNT_CONFIRM_EMAIL_ON_GET = True
    ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_URL
    ACCOUNT_USERNAME_BLACKLIST = ['admin']
    ACCOUNT_SIGNUP_FORM_CLASS = 'apps.profiles.forms.SignupForm'

    ROOT_URLCONF = 'horas.urls'

    WSGI_APPLICATION = 'horas.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3')))

    # Internationalization
    # https://docs.djangoproject.com/en/dev/topics/i18n/
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'
    HORAS_DEFAULT_TZ = os.environ.get('HORAS_DEFAULT_TZ')

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/dev/howto/static-files/
    BRUNCH_DIR = os.path.join(BASE_DIR, 'static', 'src')

    DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'

    AWS_PRELOAD_METADATA = True
    AWS_ACCESS_KEY_ID = values.Value(environ_prefix=None)
    AWS_SECRET_ACCESS_KEY = values.Value(environ_prefix=None)
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_prefix=None)

    STATIC_URL = '/static/dist/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'public')

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static', 'dist'),
    )

    SOUTH_MIGRATION_MODULES = {
        'taggit': 'taggit.south_migrations',
    }

    ANNOUNCE_TEST_MODE = False


class Development(Common):
    DEBUG = True

    TEMPLATE_DEBUG = DEBUG

    PROTOCOL = 'http'

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'debug_toolbar',
    )

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Dummy cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


class Testing(Common):
    LOGGING_CONFIG = None

    PROTOCOL = 'http'

    # Remove social logins
    INSTALLED_APPS =  [a for a in Common.INSTALLED_APPS
                        if not a.startswith('allauth.socialaccount.')]

    # Email Settings
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    # South
    SOUTH_TESTS_MIGRATE = False

    # Debug Toolbar
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    # Dummy cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    ANNOUNCE_TEST_MODE = True


class Production(Common):
    # django-secure settings
    PROTOCOL = 'https'
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'djrill',
        'raven.contrib.django.raven_compat'
    )

    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATIC_URL = 'https://d2kmfhumajdz54.cloudfront.net/'

    MANDRILL_API_KEY = values.Value(environ_prefix=None)
    DEFAULT_FROM_EMAIL = values.Value(environ_prefix=None)
    EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

    # cached sessions
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

    # Memcache setup
    os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'TIMEOUT': 1000,
            'BINARY': True,
            'OPTIONS': {
                'tcp_nodelay': True,
                'remove_failed': 4
            }
        }
    }
