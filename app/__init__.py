from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# __name__ is set to the name of the module that it is used (app) 
# flask uses module passed here as a starting point when it needs to laod associated resources
app = Flask(__name__)
app.config.from_object(Config)

# database represented from database instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login_login_view = 'login'

# place at bottom since routes module needs to import the app variable defined in this script
from app import routes, models