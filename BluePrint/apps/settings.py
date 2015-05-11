# from secret_keys import CSRF_SECRET_KEY, SESSION_KEY
from datetime import timedelta

class Config(object):	
    # Set secret keys for CSRF protection
    SECRET_KEY = "SET_YOUasdR_SECRET_KEY"
    # CSRF_SESSION_KEY = SESSION_KEY
    debug = False
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
    

class Production(Config):
    DEBUG = True
    CSRF_ENABLED = False
    ADMIN = ""
    SQLALCHEMY_DATABASE_URI = ''
    migration_directory = 'migrations'


class FacebookAPI():
    SECRET_KEY = "(!wjc0sk)S0:xc=-)KEJx-adsl"
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET = ''
    debug = True
