from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

import os
import requests
import time

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions, MobileNetV2

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

mysql = MySQL(app)

def getPrediction(filename):
    model = MobileNetV2()
    image = load_img('static/uploads/' + filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    yhat = model.predict(image)
    result = decode_predictions(yhat)[0]
    result = [(img_class, label, str(round(acc * 100, 4)) + '%') for img_class, label, acc in result]
    return result

def get_instance_info():
    try:
        service_info = requests.get("http://169.254.169.254/latest/meta-data/instance-id").text
    except:
        service_info = ''
    for i in range(7):
        flash(service_info)
    return service_info

@app.route('/')
def index():
    for i in range(16):
        flash('')
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = getPrediction(filename)
            for top_result in result:
                flash(top_result[1])
                flash(top_result[2])
            # flash(result[0][1])
            # flash(result[0][2])
            # flash(result[1][1])
            # flash(result[1][2])
            # flash(result[2][1])
            # flash(result[2][2])
            # flash(result[3][1])
            # flash(result[3][2])
            # flash(result[4][1])
            # flash(result[4][2])
            get_instance_info()
            # flash(filename)
            return render_template('index.html', filename=filename)

@app.route('/mysql')
def mysql_hello():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)