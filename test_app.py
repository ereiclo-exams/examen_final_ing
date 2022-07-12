from wsgiref import headers
import os
import tempfile
from flask_sqlalchemy import SQLAlchemy
from regex import R
import sqlalchemy
from app import app,db,Student, Singleton,csrf
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
path = '/adios'

def test_db_student_firstname(client):
    new_student = Student(firstname = 'Eric')
    db.session.add(new_student)
    db.session.commit()
    
    assert Student.query.get(1).firstname == 'Eric' 

def test_student_repr(client):
    new_student = Student(firstname = 'Eric')
    assert  new_student.__repr__() == '<Student Eric>'

def test_db_null_student(client):

    assert Student.query.all() == [] 




def test1(client):
    """Start with a blank database."""

    response = client.get('/')

    assert response.data.decode('utf-8') == 'hola'
    assert response.status_code == 200

def test2(client):
    """Start with a blank database."""

    response = client.get(token_path)
    json_data = response.get_json()

    assert 'token' in json_data 
    assert type(json_data['token']) == type("")

def test3(client):
    """Start with a blank database."""

    response = client.get('/hola')
    assert response.json['vamos a ver']  == 3

def test4(client):
    """Start with a blank database."""

    response = client.get(token_path)

    response = client.post(path,json = {
        "2": 'no',
    },headers={'X-CSRFToken':response.get_json()['token']})
    assert response.json['no vamos a ver']  == 'si' 

def test5(client):
    """Start with a blank database."""

    response = client.get(token_path)
    response = client.post(path,json = {
        "2": 'si',
    },headers={'X-CSRFToken':response.get_json()['token']})
    assert response.json['no vamos a ver']  == 'no' 

def test6(client):
    """Start with a blank database."""

    response1 = client.get(token_path)
    response = None
    data = ['1324','31412','23141']
    for i in data: 
        response = client.post('/singleton',json = {
            "data": i,
        },headers={'X-CSRFToken':response1.get_json()['token']})
    assert int(response.json['len'])  == len(data) 


def test7():
    """Start with a blank database."""
    Singleton._instance = None
    s = Singleton()
    assert s == Singleton.get_instance()



def test8():
    """Start with a blank database."""
    Singleton._instance = None
    Singleton()
    with pytest.raises(RuntimeError):
        Singleton()


def test9(client):
    """Start with a blank database."""

    response = client.get(token_path)
    response = client.post(path,json = {
        "2": 'aaa',
    },headers={'X-CSRFToken':response.get_json()['token']})
    assert response.get_json() is None

