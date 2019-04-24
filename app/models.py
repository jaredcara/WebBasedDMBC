##  models.py
##
##  This initializes all models for the database.
##  Includes User, and Job.
##

#   datetime is used to time stamp Job entries.
from datetime import datetime
#   werkzeug.security is used to secure passwords.
from werkzeug.security import generate_password_hash, check_password_hash
#   flask_login is used to allow users to remain logged into the site.
from flask_login import UserMixin

#   imports the database.
from app import db
from app import login


##  User class initializes the User model for the database
#   Columns initialized include; id, username, email, password_hash, 
#   and jobs.
class User(UserMixin, db.Model):
    # These columns are initialized with characteristics specific to their 
    # function.
    
    # id is the primary key for each database entry.
    id = db.Column(db.Integer, primary_key=True)
    # Username is a unique entry.
    username = db.Column(db.String(64), index=True, unique=True)
    # Email is a unique entry.
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # This allows jobs to be referenced back to a user.
    jobs = db.relationship('Job', backref='user', lazy='dynamic')
    
    # Returns the user type.
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # To set and generate the password hash. Enables secure password storing.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Used when logging in, to check password entry.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


##  Job class initializes the Job model for the database.
#   Columns initialized include; id, project, timestamp, useri_id, 
#   and filename.
class Job(db.Model):
    # These columns are initialized with characteristics specific to their
    # function.

    # id is the primary key for each entry.
    id = db.Column(db.Integer, primary_key=True)
    # Project stores the description of the project.
    project = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Enables back referencing to the User that submitted the data.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Stores the filename of the submitted data.
    filename = db.Column(db.String(120))
    
    # Returns the job type.
    def __repr__(self):
        return '<Job {}>'.format(self.project)


##  This user loader enables users to remain logged in to the site.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

