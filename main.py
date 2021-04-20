from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import requests
import time
import json

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions, MobileNetV2

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

inference_model = MobileNetV2()

def getPrediction(filename):
    image = load_img('static/uploads/' + filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    all_result = inference_model.predict(image)
    result = decode_predictions(all_result)[0]
    result = [(img_class, label, str(round(acc * 100, 4)) + '%') for img_class, label, acc in result]
    return result

def get_instance_info():
    try:
        # instance_ip = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", timeout=2).text
        instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=2).text
        instance_type = requests.get("http://169.254.169.254/latest/meta-data/instance-type", timeout=2).text
        avail_zone = requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone", timeout=2).text

        geo_info = requests.get('https://freegeoip.app/json')
        geo_json = json.loads(geo_info.text)

        geo_ip = geo_json['ip']
        geo_country_name = geo_json['country_name']
        geo_region_name = geo_json['region_name']
        geo_time_zone = geo_json['time_zone']
        geo_lat_lon = f"{geo_json['latitude']} / {geo_json['longitude']}"

        for info in [geo_ip, instance_id, instance_type, avail_zone,
        geo_country_name, geo_region_name, geo_time_zone, geo_lat_lon]:
            flash(info)
    except:
        for i in range(8):
            flash('Error')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    for i in range(10):
        flash('')
    get_instance_info()
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = getPrediction(filename)
            for top_result in result:
                flash(top_result[1])
                flash(top_result[2])
            get_instance_info()
            return render_template('index.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/test', methods=['POST'])
def curl_test():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'A'
        file = request.files['file']
        if file.filename == '':
            return 'B'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = getPrediction(filename)
            for top_result in result:
                print(top_result[1])
                print(top_result[2])
                # flash(top_result[1])
                # flash(top_result[2])
            # get_instance_info()
            return 'SUCCESS'
        else:
            print('ERROR')
            # flash('Allowed image types are -> png, jpg, jpeg, gif')
            return 'C'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)