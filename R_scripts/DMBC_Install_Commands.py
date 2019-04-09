print("COMMANDS FOR INSTALLING ALL PACKAGES FOR DMBC PROJECT" + "\n")

print("COMMAND TO INSTALL R:")
print("sudo -H apt-get update" + "\n" + "sudo -H apt-get install r-base" + "\n" + "sudo -H apt-get install r-base-dev" + "\n" + "sudo apt-get install libcurl4-openssl-dev" + "\n" + "sudo apt-get install libssl-dev" + "\n")

print("COMMAND TO INSTALL devtools:")
print("sudo -i R" + "\n" + "install.packages('devtools')" + "\n")

print("COMMAND TO INSTALL Flask:")
print("sudo -H pip install Flask" + "\n")

print("COMMAND TO INSTALL rpy2:")
print("sudo -H pip install rpy2==2.8.3" + "\n")

print("COMMAND TO DOWNLOAD DMBC Package:")
print("sudo -i R" + "\n" + "library(devtools)" + "\n" + "install_github('qunfengdong/DMBC')" + "\n")
