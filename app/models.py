##  models.py
##
##  This initializes all models for the database.
##  Includes User, Testing, and Training.
##

##  Import packages.
#   Datetime is used to time stamp Job entries.
from datetime import datetime
#   Werkzeug.security, and itsdangerous are used to secure passwords and reset tokens.
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#   Flask_login is used to allow users to remain logged into the site.
from flask_login import UserMixin
##  Import app functions.
#   Imports the database.
from app import app, db, login


##  User class initializes the User model for the database
#   Columns initialized include; id, username, email, password_hash, 
#   and jobs.
class User(UserMixin, db.Model):
    # These columns are initialized with characteristics specific to their 
    # function.
    
    # Id is the primary key for each database entry.
    id = db.Column(db.Integer, primary_key=True)
    # Username is a unique entry.
    username = db.Column(db.String(64), index=True, unique=True)
    # Email is a unique entry.
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # This allows jobs to be referenced back to a user.
    training = db.relationship('Training', backref='user', lazy='dynamic')
    testing = db.relationship('Testing', backref='user', lazy='dynamic')

    # Returns the user type.
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # To set and generate the password hash. Enables secure password storing.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Used when logging in, to check password entry.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


##  Training class initializes the Training model for the database.
#   Columns initialized include; id, project, timestamp, useri_id, 
#   and filename.
class Training(db.Model):
    # These columns are initialized with characteristics specific to their
    # function.

    # Id is the primary key for each entry.
    id = db.Column(db.Integer, primary_key=True)
    # Project stores the description of the project.
    project = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Ready stores status of progress.
    ready = db.Column(db.Boolean)
    # Enables back referencing to the User that submitted the data.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Stores the filename of the submitted data.
    filename = db.Column(db.String(120))
    filename_done = db.Column(db.String(120))
    # This allows the teasting to be referneced back to a training job.
    testing = db.relationship('Testing', backref='training', lazy='dynamic')
        
    # Returns the job type.
    def __repr__(self):
        return '<Training {}>'.format(self.project)


##  Testing class initializes the Testing model for the database.
#   Columns initialized include; id, project, timestamp, useri_id,
#   and filename.
class Testing(db.Model):
    # These columns are initialized with characteristics specific to their
    # function.

    # Id is the primary key for each entry.
    id = db.Column(db.Integer, primary_key=True)
    # Project stores the description of the project.
    project = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Ready stores status of progress.
    ready = db.Column(db.Boolean)
    # Enables back referencing to the User that submitted the data.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
    # Stores the filename of the submitted data.
    filename = db.Column(db.String(120))
    filename_done = db.Column(db.String(120))

    # Returns the job type.
    def __repr__(self):
        return '<Testing {}>'.format(self.project)


##  This user loader enables users to remain logged in to the site.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

