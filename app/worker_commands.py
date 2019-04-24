##  worker_commands.py
##  
##  This provides functions for the worker and queue, enables the 
##  asynchronous task management.
##


#   Imports app, database, and queue.
from app import app, db, q
#   Imports models from database.
from app.models import User, Job
#   Imports rpy2 to call the R scripts.
import rpy2.robjects as robjects


##  Training function.
#   This function calls the R scripts to load data and process the DMBC commands.
#   Accepts job_id.
def training_function(job_id):
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
        project = Job.query.get(job_id)

        # String for file path.
        location = app.instance_path + '/files/' + project.filename
        # Loads rpy2 object from rstring.
        rfunc = robjects.r(rstring)
        # Calls the rfucntion with the file location.
        rfunc(location)
    except:
        errors.append("Unable to train.")
        return {"errors": errors}

    print(errors)

