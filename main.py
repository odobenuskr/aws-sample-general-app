from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import json

import requests

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

@app.route('/')
def hello():
    return "Hello World Sungjae!"

@app.route('/<name>')
def hello_name(name):
    return f"Hello {name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)
