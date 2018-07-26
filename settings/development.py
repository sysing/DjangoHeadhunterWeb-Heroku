from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'matrix_hr_local',
        'USER': 'postgres',
        'PASSWORD': 'iamgroot',
        'HOST': 'localhost', # Or something like this
        'PORT': '5432',
    }
}
SECRET_KEY = 'g((h$7+$vvj=j@ecpj2rr(fkjl1)w$yuq(6&8=a#2y!bne4@v)'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_SSL = True
