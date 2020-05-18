import time
import os
from werkzeug.utils import cached_property
from flask import Flask, flash, request, redirect, url_for, current_app, send_from_directory
from flask_restplus import Resource, Api
from werkzeug.utils import secure_filename

from pdftoword.pdfToWord import extractFile

UPLOAD_FOLDER = 'upload'



app = Flask(__name__, static_folder=os.path.join('..', 'build', static_url_path='/'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_asdf^&j"F4Q8z\n\xec]/'
api = Api(app)

#@app.route('/time')
#def get_current_time():
#   return {'time': time.time()}

@app.route('/upload', methods=["GET","POST"])
def get_post_data():
    if request.method == "POST":
        if 'data' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['data']
        tableStart = int(request.form['tableStartPage'])
        tableEnd = int(request.form['tableEndPage'])
        pStart = int(request.form['paragraphStartPage'])
        pEnd = int(request.form['paragraphEndPage'])
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extractFile(os.path.join(app.config['UPLOAD_FOLDER'], filename), tableStart, tableEnd, pStart, pEnd)
            download_path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
            return send_from_directory(download_path, filename='output.docx')
    return "no"


if __name__ == "__main__":
    if not os.path.exists('upload'):
        os.makedirs('upload')
    app.run(debug=True)

