import os
import sys
from flask import abort
from FILEIO.TreeRead import *
from flask import make_response, jsonify
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/', methods=['GET'])
def index():
    return listDir("")

@app.route('/list/<relpath>', methods=['GET'])
def listDir(relpath):
    relativePath=relpath
    #Can only list the root now
    directory = os.path.dirname(os.path.abspath(__file__))+"/" + app.config['UPLOAD_FOLDER']
    #list directory in unix form is safer
    directory = directory.replace("\\","/")
    logging.debug("show directory:"+directory)

    if("region" in request.form ):
      region = request.form["region"]
    else:
      region=""
    print ("region:"+region)
    #else:
    #  region=""

    if(len(relpath) == 0 ):
        uploadURL=url_for('upload')
    else:
        uploadURL=url_for('upload_Path', relpath=relpath, _external=True)
    
    try:
        dlist = listPath(directory,relativePath)
    except:
        abort (404)
    for node in dlist:
        if node.isFile:
            url=url_for('get_file', filename=node.name, _external=True)
        else:
            url=url_for('listDir', relpath=node.name, _external=True)
        if(len(relativePath)>0) :
            url=url +"?relpath="+relativePath
        node.setURLPath(url)
    
    return render_template('index.html',CurrentPath=relativePath,uploadurl=uploadURL,filelst=dlist,SelectedRegion=region)

@app.route('/upload', methods=['POST'])
def upload():
    if("region" in request.form ):
      region = request.form["region"]
    else:
      region=""
    print ("regionupload:"+region)
    return upload_Path("")

# Route that will process the file upload
@app.route('/uploadpath/<relpath>', methods=['POST'])
def upload_Path(relpath):
    abspath=app.config['UPLOAD_FOLDER']
    if( len(relpath)>0):
        abspath = os.path.join(abspath, relpath)
    logging.debug("upload to:"+abspath)
    # Get the name of the uploaded file
    file = request.files['file']
    
    if("region" in request.form ):
      region = request.form["region"]
    else:
      region=""
    print ("regionupload:"+region)
    directory = os.path.dirname(os.path.abspath(__file__))+"/" + app.config['UPLOAD_FOLDER']
    
    # Check if the file is one of the allowed types/extensions
    #if file and allowed_file(file.filename):
	if file :
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(directory, filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return redirect(url_for('uploaded_file', filename=filename))
        return listDir(relpath)

@app.route('/uploadPlain', methods=['POST'])
def uploadPlain():
    abspath=app.config['UPLOAD_FOLDER']
    
    logging.debug("upload to:"+abspath)
    # Get the name of the uploaded file
    file = request.files['file']
    # Make the filename safe, remove unsupported chars
    filename = secure_filename(file.filename)
    # Move the file form the temporal folder to
    # the upload folder we setup
    file.save(os.path.join(abspath, filename))
    return "OK"
    
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/getfile/<filename>', methods=['GET'])
def get_file(filename):
    relpath=""
    abspath=app.config['UPLOAD_FOLDER']
    
    if('relpath' in request.args ):
        #logging.debug("Get File Relative path:"+request.args["relpath"])
        relpath=request.args["relpath"]
        abspath=os.path.join(abspath,relpath)
    
    directory = os.path.dirname(os.path.abspath(__file__))+"/" + app.config['UPLOAD_FOLDER']
    #list directory in unix form is safer
    directory = directory.replace("\\","/")
    
    file_path=os.path.join(directory,filename);
    logging.debug(file_path)
    if (os.path.exists(file_path) ):
        return send_from_directory(directory,filename)
    else:
        abort (404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(
        host= '0.0.0.0',
        port=int("8080"),
        debug=True
    )
