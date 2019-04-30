##  config.py
##
##  This is the config file for Flask-SQLAlchemy for this flask server.
##  'you-will-never-guess-this' should be changed for release.
##

#   Import os.
import os


#   Set base dir.
basedir = os.path.abspath(os.path.dirname(__file__))


##  Config class.
#   Sets all config variables.
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this'
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'dmbcpredict@gmail.com'
    MAIL_PASSWORD = 'compbio123'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

