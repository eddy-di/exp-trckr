# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_spectacular',
]

PROJECT_APPS = [
    'apps.users',
    'apps.finance',
]

INSTALLED_APPS += THIRD_PARTY_APPS + PROJECT_APPS
