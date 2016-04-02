import os



if 'OPENSHIFT_APP_NAME' in os.environ:
    DB_NAME = os.environ['OPENSHIFT_APP_NAME']

if 'OPENSHIFT_POSTGRESQL_DB_USERNAME' in os.environ:
    DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']

if 'OPENSHIFT_POSTGRESQL_DB_PASSWORD' in os.environ:
    DB_PASSWD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']

if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']

if 'OPENSHIFT_POSTGRESQL_DB_PORT' in os.environ:
    DB_PORT = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']

if 'MONGODB_URL' in os.environ:
    MONGODB_URL = os.environ['MONGODB_URL']

if ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pysocial',
            'USER': 'admincme1fr3',
            'PASSWORD': '7M4fRk4ByPwy',
            'HOST': DB_HOST,
            'PORT': DB_PORT
        }
    }


INSTALLED_APPS += ['users',]
