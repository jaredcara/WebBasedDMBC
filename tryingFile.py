#this file will open a webpage and allow for a file to be uploaded
#imports we need for flask in general
from flask import Flask, render_template
#imports for file stuff
from flask import flash, request, redirect, url_for
#imports for secure files
from werkzeug.utils import secure_filename
#where the upload will be stored
##UPLOAD_FOLDER = "C:\\Users\\tensm\\Desktop"
###certain extenstions allowed for file, our case is csv
##ALLOWED_EXTENSIONS = set(['csv'])
app = Flask(__name__)
##app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
##@app.route("/")
def hello():
    return "Hello World!"
 
##if __name__ == "__main__":
##    app.run()
#should just show html where we can just upload a file with the browser
#trying to figure out how to not use html
@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
#file upload_file2 because needs to have diff name
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)

#code based off of http://flask.pocoo.org/docs/1.0/patterns/fileuploads/ and https://www.tutorialspoint.com/flask/flask_file_uploading.htm
#returns server not found, very confused currently
#also will probably scrap based upon nicks comments
