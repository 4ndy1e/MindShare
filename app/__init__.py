from flask import Flask
from config import Config

# __name__ is set to the name of the module that it is used (app) 
# flask uses module passed here as a starting point when it needs to laod associated resources
app = Flask(__name__)
app.config.from_object(Config)

# place at bottom since routes module needs to import the app variable defined in this script
from app import routes