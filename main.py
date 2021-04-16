from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import requests

from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input, decode_predictions, VGG16

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def getPrediction(filename):
    model = VGG16()
    image = load_img(UPLOAD_FOLDER + '/' + filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]
    print('%s (%.2f%%)' % (label[1], label[2]*100))
    return label[1], label[2]*100

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
            print('a')
            test_label, test_acc = getPrediction(filename)
            print(test_label)
            print(test_acc)
            label, acc = 'a', 99
            flash(label)
            flash(acc)
            flash(filename)
            return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)
