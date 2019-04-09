from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfeT\xde\xfd\xedzoL\xb8\x94\x17\xc8:\x94\x82\x1e\xdb\xdc3\x91\xd1\n\xcd\x1f'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
