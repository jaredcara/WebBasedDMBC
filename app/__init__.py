from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt


app = Flask(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)


app.config.from_object(Config)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dmbcpredict@gmail.com'
app.config['MAIL_PASSWORD'] = 'compbio123'
mail = Mail(app)
mail=Mail(app)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
