from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

import os

from app import app, db, q
from app.forms import LoginForm, RegistrationForm, Upload
from app.models import User, Job
from app.worker_commands import training_function

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    all_jobs = user.jobs.all()
    jobs = []
    for each in all_jobs:
        jobs.append({'id': each.id, 'project': each.project})
    
    return render_template('user.html', user=user, jobs=jobs)


@app.route('/user/<username>/<project_id>')
@login_required
def current_project(username, project_id):
        
    return render_template('current_project.html')


@app.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    # call upload form
    form = Upload()

    # ensure the form is valid, no errors present
    if form.validate_on_submit():

        # load data into f variable and description into d variable
        f = form.upload.data
        d = form.description.data

        job = Job(project=d, user=current_user)
        db.session.add(job)
        db.session.commit()

        this_id = Job.query.filter_by(user=current_user, project=d).first().id

        filename = secure_filename(f.filename)
        filename = str(current_user.id) + '_' + str(this_id) + '_' + filename[:-4]

        f.save(os.path.join(app.instance_path, 'files', filename + '.csv'))
        
        job.filename = filename

        db.session.merge(job)
        db.session.commit()

        job = q.enqueue_call(
                func=training_function, args=(this_id,), result_ttl=5000
                )
        
        flash('File upload successful')
        return redirect(url_for('index'))
        

    return render_template('upload.html', form=form)

