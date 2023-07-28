import os
import PyPDF2
from read_pdf import pdftojson, pdftojson2
from fetch_word import give_word
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import urllib.request,json
from urllib.parse import quote  

allowed_origins = [
    'http://localhost:3003',
    'https://langapp23.onrender.com'
]

file_path = os.path.abspath(os.getcwd())+"\database.db"

app = Flask(__name__)
CORS(app, origins=allowed_origins)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400
    print(f'Hello world and hello {file.filename}')
    text, dict = pdftojson2(file)
    print(dict)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify({"message": "Flask: File uploaded successfully", "text":text,"dict":dict}), 200

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

# Add OPTIONS route to handle preflight requests
@app.route('/upload', methods=['OPTIONS'])
def handle_options_request():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/pygetword/<word>', methods=['GET'])
def pygetword(word):
    #word = request.args.get('word')
    data = give_word(word)
    response = {
        'word': data
    }
    return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/ping')
def ping():
    response = {
        'message': "It's a me, your python flask server!"
    }
    return response

if __name__ == '__main__':
    app.run()
