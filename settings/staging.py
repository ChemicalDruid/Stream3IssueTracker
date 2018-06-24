from base import *
import dj_database_url

DEBUG = False

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Load the ClearDB connection details from the environment variable
DATABASES = {
    'default': dj_database_url.config('CLEARDB_DATABASE_URL')
}

# PayPal environment variables
PAYPAL_NOTIFY_URL = 'http://codeinst-issue-tracker.herokuapp.com/a-url-that-is-difficult-to-guess/'
PAYPAL_RECEIVER_EMAIL = 'sakis.platsas-paypalmerch@gmail.com'

SITE_URL = 'https://codeinst-issue-tracker.herokuapp.com/'
ALLOWED_HOSTS.append('codeinst-issue-tracker.herokuapp.com')

# Log DEBUG information to the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}
