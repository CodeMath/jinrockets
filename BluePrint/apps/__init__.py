from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask_oauth import OAuth

import settings

app = Flask('apps')
app.config.from_object('apps.settings.Production')

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# for facebook api

oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=settings.FacebookAPI.FACEBOOK_APP_ID,
                            consumer_secret=settings.FacebookAPI.FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'}
                            )
import controllers, models