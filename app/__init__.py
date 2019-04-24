from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from rq import Queue
from rq.job import Job
from worker import conn


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

q = Queue(connection=conn)

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
