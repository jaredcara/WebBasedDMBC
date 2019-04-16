import rpy2.robjects as robjects

c = robjects.r('''
library(DMBC)
pathie <- "/home/compbio2/gjohnson6/WebBasedDMBC/R_scripts/"
direct_training <- paste(pathie, "training.csv", sep="")
training <- read.csv(file=direct_training, header=TRUE, sep=",")
Cal_AUC(loocv(training))
''')

print("loocv finished running")
print(c)
