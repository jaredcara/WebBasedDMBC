from flask import url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user



@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #the hashed password will be returend as a string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #this will show that the user that will be loging in is connected to the hashed password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #will add a new user
        db.session.add(user)
        #wil add the usuer to the database
        db.session.commit()
        flash('Your user account is created. Log in.', 'success')
        return redirect(url_for('login'))


#create the login route to check authenticated user 
#ask for the password and claim unsuccessful login 
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


