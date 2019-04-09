import rpy2.robjects as robjects

r_source = robjects.r["source"]
x = r_source("dmbc_predict_commands.R")

print("dmbc_predict finished running")
print(x)
