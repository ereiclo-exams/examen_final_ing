from wsgiref import headers
import os
import tempfile
from flask_sqlalchemy import SQLAlchemy
from regex import R
import sqlalchemy
from app import app,db,Message,csrf
import pytest


@pytest.fixture
def client():
    db_fd,path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

        yield client
    
    os.close(db_fd)
    
token_path = '/get-token'

def test_index(client):

    response = client.get('/')
    assert response.data.decode('utf-8')  == "This is an api for registering and reading messages with different topics" 
def test_message():
    message = Message(text ='me gusta el pan',topic = 'gustos')
    assert message.__repr__()  == "Message object of topic \"gustos\" with text \"me gusta el pan\""

def test_token(client):
    response = client.get(token_path)
    assert "token" in response.get_json()


def test_null_messages(client):
    # response_tok = client.get(token_path).get_json()['token']
    response = client.get('/message/gustos')
    assert response.get_json() == []

def test_3_messages(client):
    # response_tok = client.get(token_path).get_json()['token']
    for i in range(3):
        message = Message(text ='me gusta el pan',topic = 'gustos')
        db.session.add(message)
        db.session.commit()
        

    response = client.get('/message/gustos').get_json()
    assert len(response) == 3
    for m in response:
        assert m['message'] == message.text
        assert m['topic'] == message.topic



# def test6(client):

#     response1 = client.get(token_path)
#     response = None
#     data = ['1324','31412','23141']
#     for i in data: 
#         response = client.post('/singleton',json = {
#             "data": i,
#         },headers={'X-CSRFToken':response1.get_json()['token']})
#     assert int(response.json['len'])  == len(data) 



# def test4(client):
#     response = client.get(token_path)

#     response = client.post(path,json = {
#         "2": 'no',
#     },headers={'X-CSRFToken':response.get_json()['token']})
#     assert response.json['no vamos a ver']  == 'si' 

