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

#loads a page based off the html file I created
#really had to look this up cuz no idea how to do this in flask
@app.route("/")
def page():
    #opens the html file about the forms
    with open("decision.html","r") as html_file:
        #returns the read of that to the local server
        return html_file.read()

#handles all the uploading, think this only works for one file though	
@app.route('/chooseData', methods = ['GET', 'POST'])
#file upload_file2 because needs to have diff name
def choosePage():
    decision = str(request.form.get('data', None))
    if decision == "Training Data":
        return "Training"
    else:
        return "Test"
    
     
if __name__ == '__main__':
   app.run(debug = True)
  

#code based off of http://flask.pocoo.org/docs/1.0/patterns/fileuploads/ and https://www.tutorialspoint.com/flask/flask_file_uploading.htm
#returns server not found, very confused currently
#also will probably scrap based upon nicks comments
