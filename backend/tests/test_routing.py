import pytest
from mongoengine.errors import NotUniqueError, ValidationError
from models.user import User
from models.workout import Workout
from flask_jwt_extended import create_access_token
from bson import ObjectId
from werkzeug.security import generate_password_hash


""" 
User Database Routes 
"""

# Registration

def test_register_user(web_client, clear_db):
    payload = {
        "username": "Route_Testah", 
        "password" : "hashDAT"
        }
    response = web_client.post('/user', json=payload)

    assert response.status_code == 201
    assert response.json == {"message" : "Route_Testah successfully registered!"}

    user = User.objects.get(username="Route_Testah")
    assert user.username == "Route_Testah"

def test_duplicate_user_registration(web_client, clear_db):
    payload = {
        "username": "Route_Testah", 
        "password" : "hashDAT"
        }
    response = web_client.post('/user', json=payload)

    assert response.status_code == 201
    assert response.json == {"message" : "Route_Testah successfully registered!"}

    response = web_client.post('/user', json=payload)
    assert response.status_code == 409
    assert response.json['error'] == 'Username unavailable'

def test_no_password_registration_fails(web_client, clear_db):
    payload = {
        "username" : "A_User"
    }
    response = web_client.post('/user', json=payload)
    assert response.status_code == 400
    assert response.json['error'] == 'Password not provided'

def test_no_username_registration_fails(web_client, clear_db):
    payload = {
        "password" : "failure"
    }
    response = web_client.post('/user', json=payload)
    assert response.status_code == 400
    assert response.json['error'] == 'Username not provided'

# Login Routes