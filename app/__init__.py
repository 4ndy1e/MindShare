from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# __name__ is set to the name of the module that it is used (app) 
# flask uses module passed here as a starting point when it needs to laod associated resources
app = Flask(__name__)
app.config.from_object(Config)

# database represented from database instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
  if app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
      auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    secure = None
    if app.config['MAIL_USE_TLS']:
      secure = ()

    mail_handler = SMTPHandler(
      mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
      fromaddr='no-reply@' + app.config['MAIL_SERVER'],
      toaddrs = app.config['ADMINS'], subject='MindShare Failure',
      credentials = auth, secure=secure)
    
    # set level to only report errors 
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # enable file based logging
    if not os.path.exists('logs'):
      os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/mindshare.blog', maxBytes=10240, backupCount=10)

    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('MindShare startup')

# place at bottom since routes module needs to import the app variable defined in this script
from app import routes, models, errors