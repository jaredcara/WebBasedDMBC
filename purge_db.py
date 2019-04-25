##  purge_db.py
##  
##  This is only used to purge the database and its contents.
##  **Not for deployment**


#   Import database.
from app import db
#   Import database models.
from app.models import User, Testing, Training


#   Query for all contents.
for each in User.query.all():
    # Delete contents.
    db.session.delete(each)

for each in Testing.query.all():
    db.session.delete(each)

for each in Training.query.all():
    db.session.delete(each)

#   Commit session.
db.session.commit()

