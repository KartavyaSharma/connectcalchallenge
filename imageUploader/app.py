# Code based on pythonbuddy.com

import os
from flask import Flask, render_template, request, jsonify, session
from flask.helpers import url_for
from flask.wrappers import Request
from werkzeug.utils import redirect, secure_filename
import json

# Configure Flask App
# Remember to change the SECRET_KEY!

UPLOAD_LOCATION = './static/images'
ACCEPTABLE_EXTENSIONS = {'png', 'jpeg', 'gif', 'jpg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_LOCATION
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['image_data'] = {}

@app.route('/')
def index():
    """Display home page
        :return: index.html
    """
    session["count"] = 0
    return render_template('index.html', image_data=app.config['image_data'])

'''
BEGIN TASK 1
'''
# Should you use a GET or POST Request?
# @app.route('/submit_image', methods=['POST'])
# @app.route('/submit_image', methods=['GET'])

def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ACCEPTABLE_EXTENSIONS

def store_image(filename):
    with open('data.json', "r+") as json_file:
        if os.stat('data.json').st_size == 0:
            curr_json = {}
            curr_json["image_uploads"] = []
            curr_json["image_uploads"].append(filename)
            json.dump(curr_json, json_file)
            json_file.close()
        else:
            data = json.load(json_file)
            if filename in data["image_uploads"]:
                return None
            data["image_uploads"].append(filename)
            json_file.close()
            os.remove(os.getcwd()+"\\data.json")
            new_json = open('data.json', 'w')
            json.dump(data, new_json)
            new_json.close()


@app.route('/submit_image', methods=['GET', 'POST'])
def submit_image():
    """Adds an image to our server and adds it to our webpage. 
        Automatically refreshes our webpage so that user can see the image appended
    """
    if request.method == 'POST':
        f = request.files['image_to_be_uploaded']
        if f and allowed_extensions(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            store_image(filename)
        else:
            return 'File other than an image uploaded!'
        
        data = {}
        with open('data.json', "r+") as json_file:
            data = json.load(json_file)
        app.config['image_data'] = data
        return redirect(url_for('index', upload_flag=True))
        # return render_template('index.html', image_data=data)

'''
END TASK 1
'''