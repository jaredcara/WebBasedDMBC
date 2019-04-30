# WebBasedDMBC
Repo for COMP 383/483 project

DMBC is a Dirichlet-Multinomial Bayes Classifier for disease diagnosis with microbial compositions. This GitHub repo serves as our devlopment of a tool to run the DMBC R package for users online. Some functionality includes, user authentication, file upload and management, data processing, email support, and result downloading.


REQUIREMENTS:

Devlopment uisng Python3.6.7, although other versions of Python3 may work.

Current installation of R-base and R-dev.

Python venv for ease of package management. You can get by this with pip-installing all packages in the requirements.txt file.


INSTALLATION:
1. git clone https://github.com/jaredcara/WebBasedDMBC.git
2. cd WebBasedDMBC
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. sudo flask db init
7. sudo flask db migrate -m "update db"
8. flask run
*Open new terminal instance to WebBasedDMBC/*
9. python worker.py
10. Open application in your web browser!
