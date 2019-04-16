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
    with open("trainingPage.html","r") as html_file:
        #returns the read of that to the local server
        return html_file.read()

#handles all the uploading, think this only works for one file though	
@app.route('/uploadTraining', methods = ['GET', 'POST'])
#file upload_file2 because needs to have diff name
def upload_file2():
##    #need to have method to select either test or training data
##    #if user puts in both job ID and file
    #jobID = request.form['job ID']
##   # if there isn't a job ID, we will be doing trainfing data
##    if jobID is None:
##        #if the request is to post somethign to the page
    
    fTrain = request.files['file1']
    # return fTrain
        #get that file
    fTrainName = secure_filename(fTrain.filename)
    #saves the file as the filename, saves to certain directory
    fTrain.save(os.path.join(app.config['UPLOAD_FOLDER'], fTrainName))
                
    return 'Thank you for submitting your file for the DMBC trainging analysis'
           
if __name__ == '__main__':
   app.run(debug = True)
  

#code based off of http://flask.pocoo.org/docs/1.0/patterns/fileuploads/ and https://www.tutorialspoint.com/flask/flask_file_uploading.htm
#returns server not found, very confused currently
#also will probably scrap based upon nicks comments
