#this file will open a webpage and allow for a file to be uploaded
import os
#imports we need for flask in general
from flask import Flask, render_template
#imports for file stuff
from flask import flash, request, redirect, url_for
#imports for secure files
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\tensm\\Desktop'
#how to name a flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#loads a page based off the html file I created
#really had to look this up cuz no idea how to do this in flask
@app.route("/")
def page():
    #opens the html file about the forms
    with open("testPage.html","r") as html_file:
        #returns the read of that to the local server
        return html_file.read()

#handles all the uploading, think this only works for one file though	
@app.route('/uploadTest', methods = ['GET', 'POST'])
#file upload_file2 because needs to have diff name
def upload_file():
##    #need to have method to select either test or training data
##    #if user puts in both job ID and file
    #jobID = request.form['job ID']
##   # if there isn't a job ID, we will be doing trainfing data
##    if jobID is None:
##        #if the request is to post somethign to the page
    
    fTest = request.files['file2']
    # return fTrain
        #get that file
    fTestName = secure_filename(fTest.filename)
    #saves the file as the filename, saves to certain directory
    fTest.save(os.path.join(app.config['UPLOAD_FOLDER'], fTest))
    return 'Thank you for submitting your file for the DMBC testing analysis'
           
if __name__ == '__main__':
   app.run(debug = True)
  


    
