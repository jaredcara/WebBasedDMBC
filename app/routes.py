##  routes.py
## 
##  This provides all flask functionality for the front end webpage.
##  Routes include; index, login, logout, register, upload, 
##  user/<username>, and user/<username>/<project_id>.
##


##  Import packages.
#   The primary flask functions imported.
from flask import render_template, flash, redirect, url_for, request, send_file
#   The primary flask_login funcitons imported to enable login/logout.
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
#   Tools imported for parsing urls and importing filenames.
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
#   Import os.
import os
##  Import app functions.
#   Imports main app, database, and queue.
from app import app, db, q, mail, bcrypt
#   Imports database models
from app.models import User, Training, Testing
#   Imports entry forms.
from app.forms import LoginForm, RegistrationForm, UploadTraining, UploadTesting, RequestResetForm, ResetPasswordForm
#   Imports background worker functions
from app.worker_commands import training_function, testing_function


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
@app.route('/user/<username>', methods = ['GET', 'POST'])
@login_required
def user(username):
    if current_user.id != User.query.filter_by(username=username).first().id:
        flash('You do not have access to this page!')
        return redirect(url_for('index'))

    # Query the database for user.
    user = User.query.filter_by(username=username).first()
    # Query the database for the users training projects.
    all_trainings = user.training.all()
    
    # Adds all trainings to list for user to see their projects.
    trainings = []
    for each in all_trainings:
        trainings.append({'id': each.id, 'project': each.project, 'ready': each.ready, 'filename': each.filename})
    
    # Load the upload form.
    form = UploadTraining()

    # If the form is valid, submit the form.
    if form.validate_on_submit():
        # Load data into f variable and description into d variable.
        f = form.upload.data
        d = form.description.data

        # Creates new training entry for database.
        training = Training(project=d, user=current_user, ready=False)
        # Add and submit entry to database.
        db.session.add(training)
        db.session.commit()

        # Query the database for this training jpb.
        # This is to enable consistancy across input files, training is added
        # to the database first, then the id is obtained.
        training_id = Training.query.filter_by(user=current_user, project=d).first().id

        # Retrieves the filename for the input file.
        filename = secure_filename(f.filename)
        # Filenames are stored as "userid_trainingid_filename".
        filename = str(current_user.id) + '_' + str(training_id) + '_' + filename[:-4]
        # Save the file under instance/files/filename.csv.
        f.save(os.path.join(app.instance_path, 'files', filename + '.csv'))

        # Update the training database entry to include the new filename.
        training.filename = filename
        # Merge and commit the entry to the database.
        db.session.merge(training)
        db.session.commit()

        # Creates queue entry to process the uploaded data.
        # Calls the training function for the worker.
        running_job = q.enqueue_call(
                func=training_function, args=(training_id,url_for('user', username=user.username, _external=True)), result_ttl=5000
                )

        # Flash the user and return user to home.
        flash('File upload successful')
        return redirect(url_for('user', username=username))

    # Render user/<username>.
    return render_template('user.html', user=user, trainings=trainings, form=form)


##  User/<username>/<project_id> route.
#   This page is directed from user/<username>, holds all test data for a 
#   training project. Users can download the results page.
@app.route('/user/<username>/<project_id>', methods = ['GET', 'POST'])
@login_required
def current_project(username, project_id):
    if current_user.id != User.query.filter_by(username=username).first().id:
        flash('You do not have access to this page!')
        return redirect(url_for('index'))

    # Query the database for tested sets.
    training = Training.query.filter_by(id=project_id).first()
    # Query the database for the users testing sets.
    all_testings = training.testing.all()
    
    # Adds all trainings to list for users to see each testing project.
    testings = []
    for each in all_testings:
        testings.append({'id': each.id, 'project': each.project, 'ready': each.ready, 'filename': each.filename})
    
    # Load the upload form.
    form = UploadTesting()

    # If the form is valid, submit the form.
    if form.validate_on_submit():
        # Load data into f variable and description into d variable.
        f = form.upload.data
        d = form.description.data
        
        # Creates new testing entry for database.
        testing = Testing(project=d, user=current_user, training=training, ready=False)
        # Add and submit entry to database.
        db.session.add(testing)
        db.session.commit()
        
        # Query the database for this testing job.
        # This is to enable consistancy across input files, testing is added
        # to the database, then the id is obtained.
        testing_id = Testing.query.filter_by(user=current_user, project=d).first().id
        # Retrieves the filename for the input file.
        filename = secure_filename(f.filename)
        # Filenames are stored as "userid_trainingid_testingid_filename".
        filename = str(current_user.id) + '_' + str(project_id) + '_' + str(testing_id) + '_' + filename[:-4]
        # Save the file under instance/files/filename.csv.
        f.save(os.path.join(app.instance_path, 'files', filename + '.csv'))
        
        # Update the training database entry to include the new filename.
        testing.filename = filename
        # Merge and commit the entry to the database.
        db.session.merge(testing)
        db.session.commit()
        
        # Creates queue entry to process the uploaded data.
        # Calls the testing function for the worker.
        running_job = q.enqueue_call(
                func=testing_function, args=(testing_id,), result_ttl=5000
                )

        # Flash the user and return to user/<username>/<currentproject>
        flash('File upload successful')
        return redirect(url_for('current_project', username=username, project_id=project_id))

    # render user/<username>/<currentproject>
    return render_template('current_project.html', form=form, training=training.project, testings=testings)


##  Download/<filename> route.
#   This is the download route for users to download their data.
@app.route('/download/<filename>')
@login_required
def serve_file(filename):
    if Training.query.filter_by(filename=filename[:-4]).first() is not None:
        fetching_file = Training.query.filter_by(filename=filename[:-4]).first()
    elif Training.query.filter_by(filename_done=filename[:-4]).first() is not None:
        fetching_file = Training.query.filter_by(filename_done=filename[:-4]).first()
    elif Testing.query.filter_by(filename=filename[:-4]).first() is not None:
        fetching_file = Testing.query.filter_by(filename=filename[:-4]).first()
    elif Testing.query.filter_by(filename_done=filename[:-4]).first() is not None:
        fetching_file = Testing.query.filter_by(filename_done=filename[:-4]).first()
    else:
        flash('This file does not exist')
        return redirect(url_for('index'))
    
    if current_user.id != fetching_file.user_id:
        flash('You do not have access to this file!')
        return redirect(url_for('index'))

    try:
        # Filelocation foor <filename>.
        location = os.path.join(app.instance_path, 'files', filename)
        # Serve the file to the user.
        return send_file(location)
    except Exception as e:
        return str(e)


##  Download/<filename> route.
#   This is the download route for users to download the sample data.
@app.route('/sample/<filename>')
def getfile(filename):
    if filename == 'training.csv':
        try:
            location = os.path.join(app.instance_path, 'Sample', 'training.csv')
            return send_file(location)
        except Exception as e:
            return str(e)
    elif filename == 'test.csv':
        try:
            location = os.path.join(app.instance_path, 'Sample', 'test.csv')
            return send_file(location)
        except Exception as e:
            return str(e)


##  Delete/<filename> route.
#   This is the delete route for users to delete their data.
@app.route('/delete/<filename>')
@login_required
def delete_file(filename):
    file_type = 'none'
    if Training.query.filter_by(filename=filename[:-4]).first() is not None:
        fetching_file = Training.query.filter_by(filename=filename[:-4]).first()
        file_type = 'train'
    elif Testing.query.filter_by(filename=filename[:-4]).first() is not None:
        fetching_file = Testing.query.filter_by(filename=filename[:-4]).first()
        file_type = 'test'
    else:
        flash('This file does not exist')
        return redirect(url_for('index'))

    if current_user.id != fetching_file.user_id:
        flash('You do not have access to this file!')
        return redirect(url_for('index'))

    if file_type == 'train':
        for each in fetching_file.testing.all():
            os.remove(os.path.join(app.instance_path, 'files', each.filename + '.csv'))
            os.remove(os.path.join(app.instance_path, 'files', each.filename + '_done.csv'))
            db.session.delete(each)
        os.remove(os.path.join(app.instance_path, 'files', filename))
        os.remove(os.path.join(app.instance_path, 'files', filename[:-4] + '_trained.csv'))
        db.session.delete(fetching_file)
        db.session.commit()
        flash('File delete successful')
        return redirect(url_for('user', username=current_user.username))
    elif file_type == 'test':
        os.remove(os.path.join(app.instance_path, 'files', filename))
        os.remove(os.path.join(app.instance_path, 'files', filename[:-4] + '_done.csv'))
        db.session.delete(fetching_file)
        db.session.commit()
        flash('File delete successful')
        return redirect(url_for('user', username=current_user.username))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
            sender=app.config['MAIL_USERNAME'],
            recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request then ignore this email and no changes will be made.
    '''

    mail.send(msg)


@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')

        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        
        db.session.merge(user)
        db.session.commit()
        flash('Your password has been updated! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset Password', form=form)

