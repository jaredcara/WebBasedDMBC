import rpy2.robjects as robjects

r_source = robjects.r["source"]
b = r_source("FS_commands.R")

print("FS finished running")
print(b)
