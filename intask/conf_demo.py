SECRET_KEY = 'string'
DEBUG = True
ALLOWED_HOSTS = []
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db/db.sqlite3',
    }
}
