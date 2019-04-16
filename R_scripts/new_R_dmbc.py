import rpy2.robjects as robjects

x = robjects.r('''
library(DMBC)
pathie <- "/home/compbio2/gjohnson6/WebBasedDMBC/R_scripts/"
direct_training <- paste(pathie, "training.csv", sep="")
direct_test <- paste(pathie, "test.csv", sep="")
training <- read.csv(file=direct_training, header=TRUE, sep=",")
test <- read.csv(file=direct_test, header=TRUE, sep=",")
auc_out <- Cal_AUC(loocv(training))
dmbc_predict(data=training,testSet=test,auc_out=auc_out)
''')

print("dmbc_predict finished running")
print(x)

