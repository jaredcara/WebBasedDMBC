import rpy2.robjects as robjects

r_source = robjects.r["source"]
a = r_source("Cal_AUC_commands.R")

print("Cal_AUC finished running")
print(a)
