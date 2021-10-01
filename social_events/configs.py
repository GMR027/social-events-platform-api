import os
from pathlib import Path
import environ


BASE_DIR=Path(__file__).resolve().parent.parent

environment=environ.Env(
    SECRET_KEY=(str, 'key'),
    ENVIRONMENT=(str, 'localhost'),
    DB_NAME=(str, 'social_events'),
    DB_USER=(str, 'social_events'),
    DB_PASSWORD=(str, 'social_events'),
    EMAIL_HOST_USER=(str, 'john@doe.com'),
    EMAIL_HOST_PASSWORD=(str, 'password')
)

SERVER_APP_FOLDER_NAME='BACK'

environ.Env.read_env()


SECRET_KEY=environment('SECRET_KEY')
ENVIRONMENT=environment('ENVIRONMENT')
DB_NAME=environment('DB_NAME')
DB_USER=environment('DB_USER')
DB_PASSWORD=environment('DB_PASSWORD')
EMAIL_HOST_USER=environment('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=environment('EMAIL_HOST_PASSWORD')


class Common:
    SECRET_KEY=SECRET_KEY
    SITE_HEADER='Social Events CMS'
    INDEX_TITLE='CMS'
    SITE_TITLE='CMS'
    EMAIL_HOST='smtp.gmail.com'
    EMAIL_USE_TLS=True
    EMAIL_PORT=587
    DEBUG=True
    ALLOWED_HOSTS=['*']
    JWT_ACCESS_EXPIRATION_MINUTES=300
    JWT_REFRESH_EXPIRATION_MINUTES=600
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': '127.0.0.1',
            'PORT': '5432'
        }
    }
    EMAIL_HOST_USER=EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD
    ENVIRONMENT=ENVIRONMENT


class LOCAL(Common):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }
    WEB_APP_URL='http://127.0.0.1:3000/'
    MEDIA_ROOT=os.path.join(BASE_DIR, 'media')


class STAGING(Common):
    WEB_APP_URL='https://staging.social_events.com/'
    MEDIA_ROOT='/var/www/static/staging/{}/media'.format(SERVER_APP_FOLDER_NAME)


class MASTER(Common):
    DEBUG=False
    JWT_ACCESS_EXPIRATION_MINUTES=15
    JWT_REFRESH_EXPIRATION_MINUTES=30
    WEB_APP_URL='https://www.social_events.com/'
    MEDIA_ROOT='/var/www/static/staging/{}/media'.format(SERVER_APP_FOLDER_NAME)


if ENVIRONMENT == 'staging':
    env=STAGING
elif ENVIRONMENT == 'master':
    env=MASTER
else:
    env=LOCAL
