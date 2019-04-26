##  errors.py
##  
##  This is to handle errors and redirect users.
##


##  Import packages.
#   Import render_template to render pages.
from flask import render_template
#   Import app and database.
from app import app, db


#   Handler for 404, page not found.
@app.errorhandler(404)
def not_found_error(error):
    # Render 404 page.
    return render_template('404.html'), 404


#   Handler for 500, database error.
@app.errorhandler(500)
def internal_error(error):
    # Roll back database.
    db.session.rollback()
    # Render 500 page.
    return render_template('500.html'), 500

