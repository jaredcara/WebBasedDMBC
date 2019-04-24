from app.models import User, Job
from app import app, db, q
import rpy2.robjects as robjects

def training_function(job_id):
    errors = []

    try:
        rstring='''
            library(DMBC)
            function(pathie) {
                training <- read.csv(file=paste(pathie, '.csv', sep=''), header=TRUE, sep=',')
                auc_out <- Cal_AUC(loocv(training))
                write.csv(auc_out, file=paste(pathie, '_trained.csv', sep=''))
            }
        '''

        project = Job.query.get(job_id)

        location = app.instance_path + '/files/' + project.filename
        rfunc = robjects.r(rstring)
        rfunc(location)
    except:
        errors.append("Unable to train.")
        return {"errors": errors}

    print(errors)
