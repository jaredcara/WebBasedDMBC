##  worker_commands.py
##  
##  This provides functions for the worker and queue, enables the 
##  asynchronous task management.
##


#   Imports app, database, and queue.
from app import app, db, q
#   Imports models from database.
from app.models import User, Training, Testing
#   Imports rpy2 to call the R scripts.
import rpy2.robjects as robjects


##  Training function.
#   This function calls the R scripts to load data and process the DMBC commands.
#   Accepts job_id.
def training_function(training_id):
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
        training = Training.query.get(training_id).filename

        # String for file path.
        location = app.instance_path + '/files/' + training
        # Loads rpy2 object from rstring.
        rfunc = robjects.r(rstring)
        # Calls the rfucntion with the file location.
        rfunc(location)
    except:
        errors.append("Unable to train.")
        return {"errors": errors}

    print(errors)


def testing_function(testing_id):
    errors = []

    try:
        rstring='''
            library(DMBC)
            function(pathie1, pathie2, pathie3) {
                training <- read.csv(file=paste(pathie1, '.csv', sep=''), header=TRUE, sep=',')
                auc_out <- read.csv(file=paste(pathie2, '.csv', sep=''), header=TRUE, sep=',')
                testing <- read.csv(file=paste(pathie3, '.csv', sep=''), header=TRUE, sep=',')
                out <- dmbc_predict(data=training, testSet=testing, auc_out=auc_out)
                write.csv(out, file=paste(pathie3, '_done.csv', sep=''))
            }
        '''
        
        location = app.instance_path + '/files/'

        current_testing = Testing.query.get(testing_id)

        testing = location + str(current_testing.filename)
        training = location + str(current_testing.training.filename)
        trained = str(training + '_trained')

        rfunc = robjects.r(rstring)

        rfunc(training, trained, testing)
    except:
        errors.append("Unable to test.")
        print({"errors": errors})
