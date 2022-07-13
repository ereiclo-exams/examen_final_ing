import os
from crypt import methods
from re import U
from urllib import response
from flask import Flask, render_template, request, redirect, url_for, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import csrf as token_generator
from flask_wtf.csrf import CSRFProtect

import json


app = Flask(__name__)
csrf = CSRFProtect()
# csrf.init_app(app) # Compliant
app.secret_key = "12345678"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




class Message(db.Model):
    id_message = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(50),nullable = False)

    def __repr__(self):
        return f'Message object of topic \"{self.topic}\" with text \"{self.text}\"'

@app.route('/')
def index():
    return "This is an api for registering and reading messages with different topics" 

@app.route('/get-token')
def token():
    response = {"token":token_generator.generate_csrf() }
    return jsonify(response)

@app.route('/message/<topic>')
def get_message_for_topic(topic):
    response = [] 
    messages = Message.query.filter_by(topic=topic)

    for mess in messages:
        response.append({'message':mess.text,'topic':mess.topic})


    return Response(json.dumps(response),mimetype='application/json') 
    

@app.route('/message',methods=['POST'])
def create_message():

    response = {}
    json_request = request.get_json()
    if 'message' not in json_request:
        response['status'] = 'fail'
    elif 'topic' not in json_request:
        response['status'] = 'fail'
    else:
        message = Message(text = json_request['message'],topic = json_request['topic'])
        db.session.add(message)
        db.session.commit()
        response['status'] = 'ok'

    return jsonify(response)
    


if __name__ == '__main__':
    app.run(host='localhost',port=5003,debug=True)

