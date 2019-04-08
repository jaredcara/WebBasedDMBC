import rpy2.robjects as robjects

r_source = robjects.r["source"]
y = r_source("best_cm_commands.R")

print("best_cm finished running")
print(y)
