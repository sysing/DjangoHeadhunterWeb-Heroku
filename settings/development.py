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
