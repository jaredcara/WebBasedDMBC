import rpy2.robjects as robjects

r_source = robjects.r["source"]
z = r_source("CalPrb_commands.R")

print("CalPrb finished running")
print(z)
