##  __init__.py
##
##  This intializes the application instance.
##


##  Import Packages.
#   Imports Flask, Bootstrap, SQLAlchemy, Migrate, LoginManager, Config, Queue, and conn.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config
from rq import Queue
from worker import conn


#   Initalize flask and the SQLAchemy datbase.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#   Initalize bootstrap
bootstrap = Bootstrap(app)

#   Enable database migration.
migrate = Migrate(app, db)

#   Initialize queue.
q = Queue(connection=conn)

#   Initialize login manager, allows users to remain logged in.
login = LoginManager(app)
login.login_view = 'login'

#   Import models last for the database.
from app import routes, models, errors

