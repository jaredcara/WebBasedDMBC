##  routes.py
## 
##  This provides all flask functionality for the front end webpage.
##  Routes include; index, login, logout, register, upload, 
##  user/<username>, and user/<username>/<project_id>.
##

#   The main flask functions imported.
from flask import render_template, flash, redirect, url_for, request
#   The main flask_login funcitons imported to enable login/logout.
from flask_login import current_user, login_user, logout_user, login_required

#   Tools imported for parsing urls and importing filenames
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

import os

#   Imports main app, database, and queue.
from app import app, db, q
#   Imports entry forms.
from app.forms import LoginForm, RegistrationForm, Upload
#   Imports database models
from app.models import User, Job
#   Imports background worker functions
from app.worker_commands import training_function


##  Index route.
#   The home webpage.
@app.route('/')
@app.route('/index')
def index():
    # Renders index.
    return render_template('index.html', title='Home')


##  Login route.
#   Where users login.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If a user is logged in, redirect them to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Loads the login form.
    form = LoginForm()
    
    # If the form entry is valid, then submit the form.
    if form.validate_on_submit():
        # First, query the database for the entered username.
        user = User.query.filter_by(username=form.username.data).first()
        
        # If username is invalid or the password does not match entered
        # user, then redirect then for login, flash error message.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # Log in the user.
        login_user(user, remember=form.remember_me.data)
        # Redirect the user.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    # Render login page
    return render_template('login.html', title='Sign In', form=form)


##  Loutout route.
#   Where users logout.
@app.route('/logout')
def logout():
    # Logout user and redirect them to home.
    logout_user()
    return redirect(url_for('index'))


##  Register route.
#   Where users register.
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is logged in, redirect them to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Loads the registeration form.
    form = RegistrationForm()
    # If the form is valid, submit the form.
    if form.validate_on_submit():
        # Create new database entry for a user.
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Add and commit the user to the database
        db.session.add(user)
        db.session.commit()
        # Flash the user and redirect to home.
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    # Render registration page.
    return render_template('register.html', title='Register', form=form)


##  User/<username> route.
#   This is a "profile" page, users can see their current projects.
#   Requires user to be logged in.
@app.route('/user/<username>')
@login_required
def user(username):
    # Query the database for user.
    user = User.query.filter_by(username=username).first()
    # Query the database for the users jobs.
    all_jobs = user.jobs.all()
    
    # Adds all jobs to list for user to see their projects.
    jobs = []
    for each in all_jobs:
        jobs.append({'id': each.id, 'project': each.project})
    
    # Render user/<username>.
    return render_template('user.html', user=user, jobs=jobs)


##  User/<username>/<project_id> route.
#   Currently a WIP.
@app.route('/user/<username>/<project_id>')
@login_required
def current_project(username, project_id):
    return render_template('current_project.html')


##  Upload route.
#   Users upload data for a new project.
#   Requires users to be logged in.
@app.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    # Load the upload form.
    form = Upload()

    # If the form is valid, submit the form.
    if form.validate_on_submit():
        # Load data into f variable and description into d variable.
        f = form.upload.data
        d = form.description.data

        # Creates new job entry for database.
        job = Job(project=d, user=current_user)
        # Add and submit entry to database.
        db.session.add(job)
        db.session.commit()

        # Query the database for this job.
        # This is to enable consistancy across input files, job is added
        # to the database first, then the id is obtained.
        job_id = Job.query.filter_by(user=current_user, project=d).first().id
        
        # Retrieves the filename for the input file.
        filename = secure_filename(f.filename)
        # Filenames are stored as "userid_jobid_filename".
        filename = str(current_user.id) + '_' + str(job_id) + '_' + filename[:-4]
        # Save the file under instance/files/filename.csv.
        f.save(os.path.join(app.instance_path, 'files', filename + '.csv'))
        
        # Update the job database entry to include the new filename.
        job.filename = filename
        # Merge and commit the entry to the database.
        db.session.merge(job)
        db.session.commit()

        # Creates queue entry to process the uploaded data.
        # Calls the training function for the worker.
        running_job = q.enqueue_call(
                func=training_function, args=(job_id,), result_ttl=5000
                )
        
        # Flash the user and return user to home.
        flash('File upload successful')
        return redirect(url_for('index'))
        
    # Render upload page.
    return render_template('upload.html', form=form)

