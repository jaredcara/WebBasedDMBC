##  __init__.py
##
##  This intializes the application instance.
##

#   imports Flask, Config, SQLAlchemy, Migrate, LoginManager, Queue, and conn.
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from rq import Queue
from worker import conn


#   Initalize flask and the SQLAchemy datbase.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#   Enable database migration.
migrate = Migrate(app, db)

#   Initialize queue.
q = Queue(connection=conn)

#   Initialize login manager, allows users to remain logged in.
login = LoginManager(app)
login.login_view = 'login'

#   Import models last for the database.
from app import routes, models

