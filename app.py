import os
import PyPDF2
from read_pdf import pdftojson, pdftojson2
from fetch_word import give_definition, give_word2
from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import urllib.request,json
from urllib.parse import quote  


file_path = os.path.abspath(os.getcwd())+"\database.db"

app = Flask(__name__)
CORS(app) 

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    # Now, you can process the file using PyPDF2 or any other library.
    # For simplicity, we'll just return a success response here.
    print(f'Hello world and hello {file.filename}')
    text, dict = pdftojson2(file)
    print(dict)
    return jsonify({"message": "Flask: File uploaded successfully", "text":text,"dict":dict}), 200

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

@app.route('/pygetword/<word>', methods=['GET'])
def pygetword(word):
    #word = request.args.get('word')
    data = give_word2(word)
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


class ContactModel(db.Model):
    __tablename__ = "tabledsdd222ddd2dddcdddw22dddcc" #delete last 5 for partial functionality
    #__tablename__ = "table234 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False)
    word = db.Column(db.String(), unique=True)

    def __init__(self, name, word):

        # give_definition finds wiktionary definition
        self.name = name
        self.word = word

    def __repr__(self):
        return f"{self.name}"


@app.route('/ping')
def ping():
    response = {
        'message': "It's a me, your python!"
    }
    return response

@app.route('/data.json')
def data():
    return pdftojson(), 201
    # return jsonify(str(pdftojson()).replace("'",'"')), 201


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return jsonify({"success": True, "message": "this is the create endpoint"}), 201

    if request.method == 'POST':
        try:
            request_data = json.loads(request.data)
            word = request_data['word']
            name = give_definition(word)#"tauti"#request_data['word']
            contact = ContactModel(name=name, word=word)
            db.session.add(contact)
            db.session.commit()
            return jsonify({"success": True, "message": "contact added successfully"}), 201
        except:
            return jsonify({"message": name, "success": True, "message": "couldn't add"}), 201

#uploadfile in development


@app.route('/api/uploadfile', methods=['GET', 'POST'])
def receivefile():
    if request.method == 'GET':
        return jsonify({"success": True, "message": "this is the create endpoint"}), 201

    if request.method == 'POST':
        # try - uncomment to silence 500 errors
        request_data = json.loads(request.data)
        name = request_data['name']
        state = request_data['state']['selectedFile']
        #state = request_data['state']['value']
        file = open('newfilefrompython2.pdf', 'w+')
        file.write(str(state))
        file.close()
        #word = request_data['word']
        #contact = ContactModel(name=name, word=word)
        # db.session.add(contact)
        # db.session.commit()
        return jsonify({"success": True, "message": "file received", "state": state}), 201
        # except:
        #    return jsonify({"success": True, "message": "already in database"}), 201


def contact_serializer(contact):
    return {'name': contact.name, 'word': contact.word}


@app.route('/data')
def retrieveDataList():
    return jsonify([*map(contact_serializer, ContactModel.query.all())])


@app.route('/data/delete', methods=['GET', 'POST'])
def delete():
    request_data = json.loads(request.data)
    name = request_data['name']
    contact = ContactModel.query.filter_by(name=name).first()
    if request.method == 'POST':
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({"success": True, "message": "Contact deleted successfully"}), 201
        abort(404)

    return jsonify({"success": True}), 201


if __name__ == '__main__':
    app.run()
