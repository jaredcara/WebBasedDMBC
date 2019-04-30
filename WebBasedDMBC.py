##  WebBasedDMBC.py
## 
##  This function creates a shell context that adds the database instance 
##  and its models to the shell session.
##


#   Imports app and database.
from app import app, db
#   Imports database models.
from app.models import User, Testing, Training

#   Processor for application.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Testing': Testing, 'Training': Training}

