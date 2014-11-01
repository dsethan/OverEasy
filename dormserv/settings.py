"""
Django settings for dormserv project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zko6y7!iue(ik_o5$9d@4moqh8swk$_n+o0sur!qm708aab$6#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

LOCAL = False

PAY_TEST = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'restaurants',
    'demand',
    'cal',
    'item',
    'menu',
    'cart',
    'dashboard',
    'checkout',
    'payments',
    'orders',
    'home',
    'referrals',
    'userprofile',
    'kitchen',
    'drivers',
    'promotion',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dormserv.urls'

WSGI_APPLICATION = 'dormserv.wsgi.application'

# API Keys
GOOGLE_MAPS = "AIzaSyAUYyU_aUoW5iu_pZZ30U0V_bfdPHQMBQM"
STRIPE = "sk_live_dNlZsFMzrLL3XTBqJw1DRzCi"
STRIPE_PK = "pk_live_4NE8xTSIb9kJlfXpfXzZU0t4"
TWILIO_SID = "  "
TWILIO_AUTH = "d5b72594bce3487a3dff812a08bc8265"
TWILIO_PHONE = "+19195513279"

if PAY_TEST:
    STRIPE = "sk_test_jgfCdVp0nTuGAydNucnl9rjT"
    STRIPE_PK = "pk_test_SuIKPOjVOLx6pJhqOp74inWw"

# States in the USA that we are currently delivering to.

US_STATES = (
    ('North_Carolina', 'NC'),
    ('NC', 'NC'),
)

# Categories of Items that we offer:

ITEM_CATEGORIES = (
    ('Classic', 'CLA'),
    ('Pressed Juice', 'JUI'),
    ('Sides', 'SID'),
    ('Drinks', 'DRI'),
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

if not LOCAL:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Static asset configuration
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
