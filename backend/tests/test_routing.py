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

def test_successful_login_with_token(web_client, clear_db, spoofed_user, testing_password):
    payload = {
        'username' : str(spoofed_user.username),
        'password' : testing_password
    }
    response = web_client.post('/login', json=payload)

    assert response.status_code == 200
    assert response.json['message'] == f"Login successful, welcome {spoofed_user.username}"
    assert 'token' in response.json

def test_login_fails_with_bad_credentials(web_client, clear_db, testing_password):
    payload = {
        'username' : "Johnny",
        'password' : testing_password
    }
    response = web_client.post('/login', json=payload)

    assert response.status_code == 401
    assert response.json['error'] == "Invalid login credentials"
    assert 'token' not in response.json

def test_login_fails_no_username(web_client, clear_db, spoofed_user, testing_password):
    payload = {'password' : testing_password}
    response = web_client.post('/login', json=payload)

    assert response.status_code == 400
    assert response.json['error'] == "Username not provided"
    assert 'token' not in response.json

def test_login_fails_no_password(web_client, clear_db, spoofed_user):
    payload = {'username' : spoofed_user.username }

    response = web_client.post('/login', json=payload)

    assert response.status_code == 400
    assert response.json['error'] == "Password not provided"
    assert 'token' not in response.json


# User GET routes

def test_get_returns_user_list(web_client, clear_db, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = web_client.get('/users', headers=headers)
    assert response.status_code == 200
    assert 'message' in response.json.keys()

def test_get_fails_no_token(web_client, clear_db):
    response = web_client.get('users')
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'



"""
Workout routes
"""

# Workout creation

def test_workout_creates_correctly(web_client, clear_db, spoofed_user, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
            'workout_name' : "Push"
            }
    response = web_client.post('/workouts', headers=headers, json=payload)

    assert response.status_code == 201
    assert response.json['message'] == f"{payload['workout_name']} created by {spoofed_user.username}"

    user = User.objects(username=spoofed_user.username).first()
    workout = next((workout for workout in user.workout_list if workout.workout_name == "Push"), None)

    assert user.workout_list == [workout]

#TODO: Check logic on failure branches of workouts POST route