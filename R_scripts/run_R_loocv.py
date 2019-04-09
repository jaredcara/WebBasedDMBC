import rpy2.robjects as robjects

r_source = robjects.r["source"]
c = r_source("loocv_commands.R")

print("loocv finished running")
print(c)
