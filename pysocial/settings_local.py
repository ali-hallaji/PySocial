import os



if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True
if os.environ.has_key('OPENSHIFT_APP_NAME'):
    DB_NAME = os.environ['OPENSHIFT_APP_NAME']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_USERNAME'):
    DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_PASSWORD'):
    DB_PASSWD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_HOST'):
    DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_PORT'):
    DB_PORT = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']


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
