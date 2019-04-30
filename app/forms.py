##  forms.py
##
##  This initializes all forms for the flask application, these functions 
##  are used to login users, register new users, and to upload data.
##


##  Import packages.
#   Flask_wtf and wtforms are the packages used to manage forms.
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
#   Flask_login to manager logged in users.
from flask_login import current_user
##  Import database models.
#   Imports User, Training, and Testing models.
from app.models import User, Training, Testing


##  LoginForm class manages login.
#   Username, password, remember me, and submit fields.
class LoginForm(FlaskForm):
    # Validators present to reqire input data.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # BooleanField enables check box, either/or.
    remember_me = BooleanField('Remember Me')
    # Submit field.
    submit = SubmitField('Sign In')


##  RegistrationForm class manages registering new users.
#   Username, email, paswords, and submit fields.
class RegistrationForm(FlaskForm):
    # Validators present to reqire input data.
    username = StringField('Username', validators=[DataRequired()])
    # Email validator checks that email is in user@web.com format.
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # EqualTo validator checks the two passwords are equal.
    password2 = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    # Submit field.
    submit = SubmitField('Register')
    
    # Definition to validate usernames.
    # Confirms username is not used in database.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    # Definition to validate email.
    # Confirms email is not used in database.
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


##  RequestResetForm class enables requesting a password reset.
#   Email and submit fields.
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # Validate_email def checks that db has an entry for email entry.
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


##  ResetPasswordForm class enables changing a password.
#   Password and submit fields.
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


##  Upload class manages file uploads.
#   Upload and submit fields.
class UploadTraining(FlaskForm):
    # Validators present to require a file and .csv extension.
    upload = FileField(validators=[
        FileRequired(), 
        FileAllowed(['csv'], 'csv files only')
        ])
    description = StringField('Project Description')
    submit = SubmitField('Upload')
    def validate_description(self, description):
        description = Training.query.filter_by(user_id=current_user.id, project=description.data).first()
        if description is not None:
            raise ValidationError('Please use a different project description, you may have a current project with the same data.')


##  Upload class manages file uploads.
#   Upload and submit fields.
class UploadTesting(FlaskForm):
    # Validators present to require a file and .csv extension.
    upload = FileField(validators=[
        FileRequired(),
        FileAllowed(['csv'], 'csv files only')
        ])
    description = StringField('Testing Description')
    submit = SubmitField('Upload')
    def validate_description(self, description):
        description = Testing.query.filter_by(user_id=current_user.id, project=description.data).first()
        if description is not None:
            raise ValidationError('Please use a different project description, you may have a current project with the same data.')

