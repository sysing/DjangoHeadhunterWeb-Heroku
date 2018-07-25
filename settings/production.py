from .base import *

DEBUG = False
ALLOWED_HOSTS = ['tranquil-retreat-52501.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
