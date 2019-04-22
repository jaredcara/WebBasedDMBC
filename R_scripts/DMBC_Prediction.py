import rpy2.robjects as robjects
import pandas as pd
from rpy2.robjects import conversion
from rpy2.robjects import pandas2ri
pandas2ri.activate()

output = open("DMBC_Prediction.csv", "w")

training = pd.read_csv("training.csv")
test = pd.read_csv("test.csv")

training2 = pd.DataFrame.to_csv(training, sep=",", index=False, line_terminator='\n')
test2 = pd.DataFrame.to_csv(test, sep=",", index=False, line_terminator='\n')

print(training2)
print(test2)

r_training = conversion.py2ro(training2)
robjects.r.assign("my_training", r_training)
robjects.r("save(my_training, file='training.RData')")

r_test = conversion.py2ro(test2)
robjects.r.assign("my_test", r_test)
robjects.r("save(my_test, file='test.RData')")

x = robjects.r('''
library(DMBC)
load("training.RData")
training_time <- get("training")
load("test.RData")
test_time <- get("test")
auc_out <- Cal_AUC(loocv(training_time))
dmbc_predict(data=training_time,testSet=test_time,auc_out=auc_out)
''')


print("DMBC Prediction has finished running!")
print(x)
output.write(str(x))

output.close()





