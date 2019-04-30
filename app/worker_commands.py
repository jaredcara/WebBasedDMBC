##  worker_commands.py
##  
##  This provides functions for the worker and queue, enables the 
##  asynchronous task management.
##


#   Imports rpy2 to call the R scripts.
import rpy2.robjects as robjects
from flask_mail import Message
#   Imports app, database, and queue.
from app import app, db, q, mail
#   Imports models from database.
from app.models import User, Training, Testing

app.app_context().push()

def send_finished_email(training_id, url):
    user = Training.query.get(training_id).user
    jobname = Training.query.get(training_id).project
    msg = Message('Your training job has completed!',
            sender=app.config['MAIL_USERNAME'],
            recipients=[user.email])

    msg.body = f'''Hello { user.username }, 
Thank you for using DMBC. Your training job, { jobname }, has completed. Please login to your account to download your data.

{ url }

'''

    mail.send(msg)

##  Training function.
#   This function calls the R scripts to load data and process the DMBC commands.
#   Accepts job_id.
def training_function(training_id, url):
    errors = []

    try:
        # rstring is the function that will be called with rpy2.
        # Loads the DMBC library.
        # Reads training csv.
        # Calculates loocv and AUC.
        # Writes AUC to file.
        rstring='''
            library(DMBC)
            function(pathie) {
                training <- read.csv(file=paste(pathie, '.csv', sep=''), header=TRUE, sep=',')
                auc_out <- Cal_AUC(loocv(training))
                write.csv(auc_out, file=paste(pathie, '_trained.csv', sep=''))
            }
        '''
        
        # Query database for the job.
        training = Training.query.get(training_id)
        
        # String for file path.
        location = app.instance_path + '/files/' + training.filename
        
        # Loads rpy2 object from rstring.
        rfunc = robjects.r(rstring)
        # Calls the rfucntion with the file location.
        rfunc(location)
        
        # Set database entry to show training is completed.
        training.ready = True
        training.filename_done = training.filename + '_trained'
        # Merge and commit training change.
        db.session.merge(training)
        db.session.commit()
        
        send_finished_email(training_id, url)
    except:
        errors.append("Unable to train.")
        return {"errors": errors}


def testing_function(testing_id):
    errors = []

    try:
        # rstring is the function that will be called with rpy2.
        # Loads the DMBC library.
        # Reads training, auc_out, and testing csv.
        # Calculates the testing results.
        # Writes out to file.
        rstring='''
            library(DMBC)
            function(pathie1, pathie2, pathie3, pathie4) {
                training <- read.csv(file=paste(pathie1, '.csv', sep=''), header=TRUE, sep=',')
                auc_out <- read.csv(file=paste(pathie2, '.csv', sep=''), header=TRUE, sep=',')
                testing <- read.csv(file=paste(pathie3, '.csv', sep=''), header=TRUE, sep=',')
                out <- dmbc_predict(data=training, testSet=testing, auc_out=auc_out)
                write.csv(out, file=paste(pathie4, '.csv', sep=''))
            }
        '''
        
        # Query database for the job.
        current_testing = Testing.query.get(testing_id)
        
        # String for file path.
        location = app.instance_path + '/files/'
        # Strings for each input file.
        training = location + str(current_testing.training.filename)
        trained = location + str(current_testing.training.filename_done)
        testing = location + str(current_testing.filename)
        tested = location + str(current_testing.filename) + '_done'

        # Loads rpy2 object from rstring.
        rfunc = robjects.r(rstring)
        # Calls the rfunction with the file locations.
        rfunc(training, trained, testing, tested)
        
        # Set the database entry to show testing is completed.
        current_testing.ready = True
        current_testing.filename_done = str(current_testing.filename) + '_done'
        # Merge and commit testing change.
        db.session.merge(current_testing)
        db.session.commit()

    except:
        errors.append("Unable to test.")
        return {"errors": errors}

