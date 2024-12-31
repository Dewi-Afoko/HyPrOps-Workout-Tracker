import pytest
from mongoengine.errors import NotUniqueError, ValidationError
from models.user import User
from models.workout import Workout
from flask_jwt_extended import create_access_token
from bson import ObjectId
from werkzeug.security import generate_password_hash
from lib.utilities.api_functions import find_single_workout
from datetime import datetime

""" 
User Database Routes 
"""

# Registration

def test_register_user(web_client, clear_db):
    payload = {
        "username": "Route_Testah", 
        "password" : "hashDAT"
        }
    response = web_client.post('/api/users', json=payload)

    assert response.status_code == 201
    assert response.json == {"message" : "Route_Testah successfully registered!"}

    user = User.objects.get(username="Route_Testah")
    assert user.username == "Route_Testah"

def test_duplicate_user_registration(web_client, clear_db):
    payload = {
        "username": "Route_Testah", 
        "password" : "hashDAT"
        }
    response = web_client.post('/api/users', json=payload)

    assert response.status_code == 201
    assert response.json == {"message" : "Route_Testah successfully registered!"}

    response = web_client.post('/api/users', json=payload)
    assert response.status_code == 409
    assert response.json['error'] == 'Username unavailable'

def test_no_password_registration_fails(web_client, clear_db):
    payload = {
        "username" : "A_User"
    }
    response = web_client.post('/api/users', json=payload)
    assert response.status_code == 400
    assert response.json['error'] == 'Password not provided'

def test_no_username_registration_fails(web_client, clear_db):
    payload = {
        "password" : "failure"
    }
    response = web_client.post('/api/users', json=payload)
    assert response.status_code == 400
    assert response.json['error'] == 'Username not provided'




# Login Routes

def test_successful_login_with_token(web_client, clear_db, user_burrito, testing_password):
    payload = {
        'username' : str(user_burrito.username),
        'password' : testing_password
    }
    response = web_client.post('/api/login', json=payload)


    assert response.status_code == 200
    assert response.json['message'] == f"Login successful, welcome {user_burrito.username}"
    assert 'token' in response.json

def test_login_fails_with_bad_username(web_client, clear_db, testing_password):
    payload = {
        'username' : "Johnny",
        'password' : testing_password
    }
    response = web_client.post('/api/login', json=payload)

    assert response.status_code == 401
    assert response.json['error'] == "User not found"
    assert 'token' not in response.json

def test_login_fails_with_bad_password(web_client, clear_db, user_burrito):
    payload = {
        'username' : str(user_burrito.username),
        'password' : "Not the password"
    }
    response = web_client.post('/api/login', json=payload)

    assert response.status_code == 401
    assert response.json['error'] == "Invalid login credentials"
    assert 'token' not in response.json

def test_login_fails_no_username(web_client, clear_db, user_burrito, testing_password):
    payload = {'password' : testing_password}
    response = web_client.post('/api/login', json=payload)

    assert response.status_code == 400
    assert response.json['error'] == "Username not provided"
    assert 'token' not in response.json

def test_login_fails_no_password(web_client, clear_db, user_burrito):
    payload = {'username' : user_burrito.username }

    response = web_client.post('/api/login', json=payload)

    assert response.status_code == 400
    assert response.json['error'] == "Password not provided"
    assert 'token' not in response.json


# User GET routes

def test_get_returns_user_list(web_client, clear_db, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = web_client.get('/api/users', headers=headers)
    assert response.status_code == 200
    assert 'message' in response.json.keys()

def test_get_fails_no_token(web_client, clear_db):
    response = web_client.get('/api/users')
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'



"""
Workout routes
"""

# Workout creation



def test_workout_creates_correctly(web_client, clear_db, user_burrito, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
            'workout_name' : "Push"
            }
    response = web_client.post('/api/workouts', headers=headers, json=payload)

    assert response.status_code == 201
    assert response.json['message'] == f"{payload['workout_name']} created by {user_burrito.username}"

    workout = Workout.objects(user_id=str(user_burrito.id)).first()

    assert workout.user_id == user_burrito

def test_workout_fails_with_no_name(web_client, clear_db, user_burrito, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {'incorrect key' : 'invalid value'}

    response = web_client.post('/api/workouts', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json['error'] == "You need to name your workout"

def test_workout_fails_with_bad_user_token(web_client, clear_db, bad_token):
    headers = {"Authorization": f"Bearer {bad_token}"}
    payload = {
            'workout_name' : "Push"
            }

    response = web_client.post('/api/workouts', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json['error'] == 'User not found'



# GET User Workouts

def test_getting_user_workouts_success(web_client, clear_db, user_burrito, burrito_workout, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = web_client.get('/api/workouts', headers=headers)        
        assert response.json['message'] == 'Here are your workouts:'
        assert 'workouts' in response.json
        assert response.status_code == 200

                    
def test_getting_workouts_fails_with_no_workouts(web_client, clear_db, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = web_client.get('/api/workouts', headers=headers)    

        assert response.json['error'] == 'No workouts found'
        assert response.status_code == 404     
                    
                    
                    
def test_getting_single_workout_success(web_client, clear_db, auth_token, user_burrito, burrito_workout):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(burrito_workout.id)
        response = web_client.get(f'/api/workouts/{workout_id}', headers=headers)

        assert response.json['message'] == f'Here are the details for workout ID: {workout_id}'
        assert response.json['workout'] == burrito_workout.to_dict()
        assert response.status_code == 200   

def test_getting_single_workout_success_with_multiple_workouts(web_client, clear_db, auth_token, user_burrito, burrito_workout):
        headers = {"Authorization": f"Bearer {auth_token}"}
        web_client.post('/api/workouts', headers=headers, json={'workout_name' : 'Workout2'})
        web_client.post('/api/workouts', headers=headers, json={'workout_name' : 'Workout3'})
        workout_id = str(burrito_workout.id)

        response = web_client.get('/api/workouts', headers=headers) 
        assert len(response.json['workouts']) == 3

        response = web_client.get(f'/api/workouts/{workout_id}', headers=headers)

        assert response.json['message'] == f'Here are the details for workout ID: {workout_id}'
        assert response.json['workout'] == burrito_workout.to_dict()
        assert response.status_code == 200   

def test_add_notes_to_workout(web_client, clear_db, auth_token, burrito_workout):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(burrito_workout.id)
        payload = {'notes' : 'Adding more notes'}

        assert len(burrito_workout.notes) == 1

        response = web_client.patch(f'/api/workouts/{workout_id}/add_notes', headers=headers, json=payload)

        assert response.json['message'] == f'{payload["notes"]}: added to workout notes'
        assert response.status_code == 200
        burrito_workout.reload()
        assert len(burrito_workout.notes) == 2

def test_delete_notes_from_workout(web_client, clear_db, auth_token, burrito_workout):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(burrito_workout.id)
        payload = {'notes' : 'Adding more notes'}

        assert len(burrito_workout.notes) == 1
        web_client.patch(f'/api/workouts/{workout_id}/add_notes', headers=headers, json={'notes' : 'Persist these notes'})
        response = web_client.patch(f'/api/workouts/{workout_id}/add_notes', headers=headers, json=payload)
        web_client.patch(f'/api/workouts/{workout_id}/add_notes', headers=headers, json={'notes' : 'Persist these notes'})

        burrito_workout.reload()

        assert response.json['message'] == f'{payload["notes"]}: added to workout notes'
        assert response.status_code == 200
        assert len(burrito_workout.notes) == 4

        note_index = 2
        response = web_client.delete(f'/api/workouts/{workout_id}/delete_note/{note_index}', headers=headers)
        assert response.status_code == 200
        assert response.json['message'] == 'Note successfully deleted'

        burrito_workout.reload()

        assert len(burrito_workout.notes) == 3
        assert burrito_workout.notes[1] == 'Persist these notes'
        assert burrito_workout.notes[2] == 'Persist these notes'


def test_toggling_workout_complete(web_client, clear_db, auth_token, burrito_workout):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(burrito_workout.id)
        assert burrito_workout.complete == False
        response = web_client.patch(f'/api/workouts/{workout_id}/mark_complete', headers=headers)
        burrito_workout.reload()
        assert response.json['message'] == "Workout marked as complete"
        assert response.status_code == 200
        assert burrito_workout.complete == True
        response = web_client.patch(f'/api/workouts/{workout_id}/mark_complete', headers=headers)
        assert response.json['message'] == "Workout marked as incomplete"
        assert response.status_code == 200
        burrito_workout.reload()
        assert burrito_workout.complete == False
                    


### FUNCTIONALITY: Workout x SetDict Tests

def test_adding_set_dict_success(web_client, clear_db, auth_token, burrito_workout, warm_up_shoulder_press):
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_id = str(burrito_workout.id)
    payload = {
                'exercise_name': warm_up_shoulder_press.exercise_name,
                'set_type' : warm_up_shoulder_press.set_type,
                'reps': warm_up_shoulder_press.reps,
                'loading': warm_up_shoulder_press.loading,
                'focus' : warm_up_shoulder_press.focus,
                'rest' : warm_up_shoulder_press.rest,
                'notes' :warm_up_shoulder_press.notes
            }
    response = web_client.post(f'/api/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict in workout

    burrito_workout.reload()

    assert response.json['message'] == f"Set info for {payload['exercise_name']} created and added to {str(burrito_workout.workout_name)}"
    assert response.status_code == 201
    burrito_workout.reload()


    assert len(burrito_workout.set_dicts_list) == 1
    

def test_no_exercise_name_set_dict_fails(web_client, clear_db, user_burrito, warm_up_shoulder_press, burrito_workout, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_id = str(burrito_workout.id)
    payload = {
                'set_type' : warm_up_shoulder_press.set_type,
                'reps': warm_up_shoulder_press.reps,
                'loading': warm_up_shoulder_press.loading,
                'focus' : warm_up_shoulder_press.focus,
                'rest' : warm_up_shoulder_press.rest,
                'notes' :warm_up_shoulder_press.notes
            }

    response = web_client.post(f'/api/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict
    
    assert response.json['error'] == "You need to specify an exercise"
    assert response.status_code == 400



def test_partial_set_dict_creation_succeess(web_client, clear_db, auth_token, user_burrito, burrito_workout, warm_up_shoulder_press):
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_id = str(burrito_workout.id)
    payload = {
                'exercise_name': warm_up_shoulder_press.exercise_name,
                'reps': warm_up_shoulder_press.reps,
                'loading': warm_up_shoulder_press.loading,
                'rest' : warm_up_shoulder_press.rest,
                'notes' :warm_up_shoulder_press.notes
            }

    response = web_client.post(f'/api/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict

    burrito_workout.reload()

    assert response.json['message'] == f"Set info for {payload['exercise_name']} created and added to {burrito_workout.workout_name}"
    assert response.status_code == 201

    assert len(burrito_workout.set_dicts_list) == 1

def test_creation_of_set_dict_fails_with_invalid_inputs(web_client, clear_db, user_burrito, auth_token, burrito_workout, warm_up_shoulder_press):
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_id = str(burrito_workout.id)
    payload = {
                'exercise_name': warm_up_shoulder_press.exercise_name,
                'set_type' : warm_up_shoulder_press.set_type,
                'reps': warm_up_shoulder_press.reps,
                'loading': warm_up_shoulder_press.loading,
                'focus' : 12,
                'rest' : warm_up_shoulder_press.rest,
                'notes' :warm_up_shoulder_press.notes
            }


    response = web_client.post(f'/api/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict

    assert response.json['error'] == 'Failure to create set dictionary'
    assert response.status_code == 400


def test_set_dict_toggle_complete_twice(web_client, clear_db, auth_token, workout_with_dicts):
    headers = {"Authorization": f"Bearer {auth_token}"}
    assert workout_with_dicts.set_dicts_list[0].complete == False
    workout_id = str(workout_with_dicts.id)
    set_order = 1
    response = web_client.patch(f'/api/workouts/{workout_id}/{set_order}/mark_complete', headers=headers)
    assert response.json['message'] == 'Set marked complete'
    assert response.status_code == 200
    workout_with_dicts.reload()
    assert workout_with_dicts.set_dicts_list[0].complete == True
    response = web_client.patch(f'/api/workouts/{workout_id}/{set_order}/mark_complete', headers=headers)
    assert response.json['message'] == 'Set marked incomplete'
    assert response.status_code == 200
    workout_with_dicts.reload()
    assert workout_with_dicts.set_dicts_list[0].complete == False


def test_set_dict_add_notes(web_client, auth_token, clear_db, workout_with_dicts):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {'notes' : 'Until failure'}
    workout_id = str(workout_with_dicts.id)
    set_order = workout_with_dicts.set_dicts_list[0].set_order

    response = web_client.patch(f'/api/workouts/{workout_id}/{set_order}/add_notes', headers=headers, json=payload)
    assert response.json['message'] == "Notes added to set"
    assert response.status_code == 201
    workout_with_dicts.reload()

    updated_notes = workout_with_dicts.set_dicts_list[0].notes
    assert updated_notes == "Until failure"

def test_set_dict_delete_notes(web_client, auth_token, clear_db, workout_with_dicts):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {'notes' : 'Until failure'}
    workout_id = str(workout_with_dicts.id)
    set_order = workout_with_dicts.set_dicts_list[0].set_order

    response = web_client.patch(f'/api/workouts/{workout_id}/{set_order}/add_notes', headers=headers, json=payload)
    assert response.json['message'] == "Notes added to set"
    assert response.status_code == 201
    workout_with_dicts.reload()
    assert len(workout_with_dicts.set_dicts_list[0].notes) > 0

    response = web_client.delete(f'/api/workouts/{workout_id}/{set_order}/delete_notes', headers=headers)
    assert response.json['message'] == "Notes deleted"
    assert response.status_code == 200

    workout_with_dicts.reload()
    assert workout_with_dicts.set_dicts_list[0].notes == None

def test_updating_user_personal_details(web_client, auth_token, user_burrito, clear_db):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "name" : "Zan Ji",
        "dob" : "2023/01/01",
        "weight" : 30,
        "height" : 25
    }
    response = web_client.patch('/api/users/update_personal_data', headers=headers, json=payload)
    assert response.json['message'] == "Personal data updated"
    assert response.status_code == 201
    user_burrito.reload()
    assert user_burrito.name == "Zan Ji"
    assert user_burrito.weight[datetime.now().strftime("%Y/%m/%d")] ==  30
    assert user_burrito.height == 25
    assert user_burrito.to_dict()['dob'] == "2023/01/01"
