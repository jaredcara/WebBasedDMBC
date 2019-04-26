#TAYLORS NOTES: we need some functionality with the test.csv in the direct_test
#I am unsure how we are differentiating bwtween the test and training
#See notes above diff function

#import rpy2
#need this to run R scripts (DMBC code) in python
import rpy2.robjects as robjects
#imports to be able to use the database
from app import app, db
from app.models import User, Job

#some functionality for the transfer of the job database
#job becomes the list of lists that is equivalent to outp from routes.py 
jobs = [[]]
#opens file to write out to
#making new cvs to run through thee R scripts
with open("DMBCrun.csv","w") as runFile:
    for i in jobs:
        for j in range(0,len(jobs[i])-1):
            if j < len(jobs[i]) -1:
                runFile.write(str(jobs[i[j]])+ ",")
            else:
                runFile.write(str(jobs[i[j]]) + '\n')
#runs the rScript using the new DMBCrun file, this just runs everything
#in reality, we do not need to run all at once
#see the commands for parts below
x = robjects.r('''
library(DMBC)
pathie <- "/home/compbio2/gjohnson6/WebBasedDMBC/R_scripts/"
direct_training <- paste(pathie, "DMBCrun.csv", sep="")
direct_test <- paste(pathie, "test.csv", sep="")
training <- read.csv(file=direct_training, header=TRUE, sep=",")
test <- read.csv(file=direct_test, header=TRUE, sep=",")
auc_out <- Cal_AUC(loocv(training))
dmbc_predict(data=training,testSet=test,auc_out=auc_out)
''')

#COMMANDS FOR INDIVIDUAL PARTS

#to run the script and just get auc_out back for the database
#therefore, this runs everything for training
Cal_AUCOut = robjects.r('''
library(DMBC)
pathie <- "/home/compbio2/gjohnson6/WebBasedDMBC/R_scripts/"
direct_training <- paste(pathie, "DMBCrun.csv", sep="")
training <- read.csv(file=direct_training, header=TRUE, sep=",")
auc_out <- Cal_AUC(loocv(training))
''')


#to run the script later with the test data
#NEED to use above file funcionality with test file
#NEED to resolve dmbc_predict line, get Cal_AUCOut from db
#how auc_out = CalAUCOut
DMBCPrediction = robjects.r('''
library(DMBC)
pathie <- "/home/compbio2/gjohnson6/WebBasedDMBC/R_scripts/"
direct_test <- paste(pathie, "test.csv", sep="")
test <- read.csv(file=direct_test, header=TRUE, sep=",")
dmbc_predict(data=training,testSet=test,auc_out=auc_out)
''')
