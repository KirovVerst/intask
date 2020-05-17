SECRET_KEY = 'string'
DEBUG = True
ALLOWED_HOSTS = []

# Email configuration
EMAIL_SETTINGS = {
    "address": "email@email.com",
    "domain_name": "123.mailgun.org",
    "api_key": "key"
}
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db/db.sqlite3',
    }
}
