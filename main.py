from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import requests

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            label, acc = 'dog', 99.99
            flash(label)
            flash(acc)
            flash(filename)
            return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)
