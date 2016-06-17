# Import some utility functions
from os.path import join
# Fetch our common settings
from common import *

# #########################################################

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS + [
        "django_extensions",
        ]


# CORS configuration
# The following probably shouldn't be hardcoded.
# See below for docs:
# https://github.com/ottoyiu/django-cors-headers/blob/master/README.md
CORS_ORIGIN_REGEX_WHITELIST = ('^https?://localhost:.*')
CORS_URLS_REGEX = r'^/(api/|api-auth/).*'
