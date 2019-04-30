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
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from config import Config
from rq import Queue
from worker import conn


#   Initalize flask and the SQLAchemy datbase.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#   Enable database migration.
migrate = Migrate(app, db)

#   Initialize login manager, allows users to remain logged in.
login = LoginManager(app)
login.login_view = 'login'

#   Initalize bootstrap
bootstrap = Bootstrap(app)

bcrypt = Bcrypt(app)

mail = Mail(app)

q = Queue(connection=conn)

def create_app(config_class=Config):
    #   Initalize flask and the SQLAchemy datbase.
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = Queue('Tasks', connection=conn)
    


    return app


#   Import models last for the database.
from app import routes, models, errors

