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

def test_workout_fails_with_no_name(web_client, clear_db, spoofed_user, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {'incorrect key' : 'invalid value'}

    response = web_client.post('/workouts', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json['error'] == "You need to name your workout"

def test_workout_fails_with_bad_user_token(web_client, clear_db, bad_token):
    headers = {"Authorization": f"Bearer {bad_token}"}
    payload = {
            'workout_name' : "Push"
            }

    response = web_client.post('/workouts', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json['error'] == 'User not found'



# GET User Workouts

def test_getting_user_workouts_success(web_client, clear_db, spoofed_populated_user, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = web_client.get('/workouts', headers=headers)

        assert response.json['message'] == 'Here are your workouts:'
        assert 'workouts' in response.json
        assert response.status_code == 200

                    
def test_getting_workouts_fails_with_no_workouts(web_client, clear_db, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = web_client.get('/workouts', headers=headers)    

        assert response.json['error'] == 'No workouts found'
        assert response.status_code == 400         
                    
                    
                    
def test_getting_single_workout_success(web_client, clear_db, auth_token, spoofed_populated_user):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(spoofed_populated_user.workout_list[0].id)
        response = web_client.get(f'/workouts/{workout_id}', headers=headers)

        assert response.json['message'] == f'Here are the details for workout ID: {workout_id}'
        assert response.json['workout'] == spoofed_populated_user.workout_list[0].to_dict()
        assert response.status_code == 200   

def test_getting_single_workout_success_with_multiple_workouts(web_client, clear_db, auth_token, spoofed_populated_user):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(spoofed_populated_user.workout_list[0].id)
        web_client.post('/workouts', headers=headers, json={'workout_name' : 'Workout2'})
        web_client.post('/workouts', headers=headers, json={'workout_name' : 'Workout3'})
        spoofed_populated_user.reload()

        assert len(spoofed_populated_user.workout_list) == 3

        response = web_client.get(f'/workouts/{workout_id}', headers=headers)

        assert response.json['message'] == f'Here are the details for workout ID: {workout_id}'
        assert response.json['workout'] == spoofed_populated_user.workout_list[0].to_dict()
        assert response.status_code == 200   

def test_add_notes_to_workout(web_client, clear_db, auth_token, spoofed_populated_user):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(spoofed_populated_user.workout_list[0].id)
        payload = {'notes' : 'Adding more notes'}

        assert len(spoofed_populated_user.workout_list[0].notes) == 0

        response = web_client.patch(f'/workouts/{workout_id}/add_notes', headers=headers, json=payload)

        assert response.json['message'] == f'{payload["notes"]}: added to workout notes'
        assert response.status_code == 202

        spoofed_populated_user.reload()

        assert len(spoofed_populated_user.workout_list[0].notes) == 1

def test_delete_notes_from_workout(web_client, clear_db, auth_token, spoofed_populated_user):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(spoofed_populated_user.workout_list[0].id)
        payload = {'notes' : 'Adding more notes'}

        assert len(spoofed_populated_user.workout_list[0].notes) == 0
        web_client.patch(f'/workouts/{workout_id}/add_notes', headers=headers, json={'notes' : 'Persist these notes'})
        response = web_client.patch(f'/workouts/{workout_id}/add_notes', headers=headers, json=payload)
        web_client.patch(f'/workouts/{workout_id}/add_notes', headers=headers, json={'notes' : 'Persist these notes'})

        spoofed_populated_user.reload()

        assert response.json['message'] == f'{payload["notes"]}: added to workout notes'
        assert response.status_code == 202
        assert len(spoofed_populated_user.workout_list[0].notes) == 3

        spoofed_populated_user.reload()
        note_index = 1
        response = web_client.delete(f'/workouts/{workout_id}/delete_note/{note_index}', headers=headers)
        assert response.status_code == 202
        assert response.json['message'] == 'Note successfully deleted'


        spoofed_populated_user.reload()
        assert len(spoofed_populated_user.workout_list[0].notes) == 2
        assert spoofed_populated_user.workout_list[0].notes[0] == 'Persist these notes'
        assert spoofed_populated_user.workout_list[0].notes[1] == 'Persist these notes'


def test_toggling_workout_complete(web_client, clear_db, auth_token, spoofed_populated_user):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_id = str(spoofed_populated_user.workout_list[0].id)
        assert spoofed_populated_user.workout_list[0].complete == False
        response = web_client.patch(f'/workouts/{workout_id}/mark_complete', headers=headers)
        spoofed_populated_user.reload()
        assert response.json['message'] == "Workout marked as complete"
        assert response.status_code == 201
        assert spoofed_populated_user.workout_list[0].complete == True
        response = web_client.patch(f'/workouts/{workout_id}/mark_complete', headers=headers)
        assert response.json['message'] == "Workout marked as incomplete"
        assert response.status_code == 201
        spoofed_populated_user.reload()
        assert spoofed_populated_user.workout_list[0].complete == False
                    

def test_adding_userstats_to_workout(web_client, clear_db, auth_token, spoofed_populated_user, alt_spoofed_user_stats, spoofed_user_stats):
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_id = str(spoofed_populated_user.workout_list[0].id)
    assert spoofed_populated_user.workout_list[0].user_stats == spoofed_user_stats
    print(f'{alt_spoofed_user_stats.to_dict() =}')
    payload = alt_spoofed_user_stats.to_dict()
    response = web_client.put(f'/workouts/{workout_id}/add_stats', headers=headers, json=payload)
    assert response.json['message'] == 'Stats added to workout'
    assert response.status_code == 201
    spoofed_populated_user.reload()
    assert spoofed_populated_user.workout_list[0].user_stats == alt_spoofed_user_stats




                    ### Workout x SetDict Tests

def test_adding_set_dict_success(web_client, clear_db, auth_token, spoofed_user, spoof_arnold_press_dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    web_client.post('/workouts', headers=headers, json={'workout_name' : 'First Try'}) # Create Workout
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    workout_id = str(workout.id)
    payload = {
                'exercise_name': spoof_arnold_press_dict.exercise_name,
                'set_type' : spoof_arnold_press_dict.set_type,
                'reps': spoof_arnold_press_dict.reps,
                'loading': spoof_arnold_press_dict.loading,
                'focus' : spoof_arnold_press_dict.focus,
                'rest' : spoof_arnold_press_dict.rest,
                'notes' :spoof_arnold_press_dict.notes
            }
    response = web_client.post(f'/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict in workout

    spoofed_user.reload()

    assert response.json['message'] == f"Set info for {payload['exercise_name']} created and added to {str(workout.workout_name)}"
    assert response.status_code == 201
    spoofed_user.reload()

    workout_to_check = next((workout for workout in spoofed_user.workout_list if str(workout.id) == workout_id), None) # Fetch the workout_list from spoofed user embedded listfield

    assert len(workout_to_check.set_dicts_list) == 1
    

def test_no_exercise_name_set_dict_fails(web_client, clear_db, spoofed_user, spoof_arnold_press_dict, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    web_client.post('/workouts', headers=headers, json={'workout_name' : 'First Try'}) # Create Workout
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    workout_id = str(workout.id)
    payload = {
                'set_type' : spoof_arnold_press_dict.set_type,
                'reps': spoof_arnold_press_dict.reps,
                'loading': spoof_arnold_press_dict.loading,
                'focus' : spoof_arnold_press_dict.focus,
                'rest' : spoof_arnold_press_dict.rest,
                'notes' :spoof_arnold_press_dict.notes
            }

    response = web_client.post(f'/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict
    
    assert response.json['error'] == "You need to specify an exercise"
    assert response.status_code == 400



def test_partial_set_dict_creation_succeess(web_client, clear_db, auth_token, spoofed_user, spoofed_empty_workout, spoof_arnold_press_dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    web_client.post('/workouts', headers=headers, json={'workout_name' : 'First Try'}) # Create Workout
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    workout_name = str(workout.workout_name)
    workout_id = str(workout.id)
    payload = {
                'exercise_name': spoof_arnold_press_dict.exercise_name,
                'reps': spoof_arnold_press_dict.reps,
                'loading': spoof_arnold_press_dict.loading,
                'rest' : spoof_arnold_press_dict.rest,
                'notes' :spoof_arnold_press_dict.notes
            }

    response = web_client.post(f'/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict

    spoofed_user.reload()

    assert response.json['message'] == f"Set info for {payload['exercise_name']} created and added to {workout_name}"
    assert response.status_code == 201

    workout_to_check = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None) # Fetch the workout_list from spoofed user embedded listfield

    assert len(workout_to_check.set_dicts_list) == 1

def test_creation_of_set_dict_fails_with_invalid_inputs(web_client, clear_db, spoofed_user, auth_token, spoofed_empty_workout, spoof_arnold_press_dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    web_client.post('/workouts', headers=headers, json={'workout_name' : 'First Try'}) # Create Workout
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    workout_id = str(workout.id)
    payload = {
                'workout_name' : spoofed_empty_workout.workout_name,
                'exercise_name': spoof_arnold_press_dict.exercise_name,
                'set_type' : spoof_arnold_press_dict.set_type,
                'reps': spoof_arnold_press_dict.reps,
                'loading': spoof_arnold_press_dict.loading,
                'focus' : 12,
                'rest' : spoof_arnold_press_dict.rest,
                'notes' :spoof_arnold_press_dict.notes
            }


    response = web_client.post(f'/workouts/{workout_id}/add_set', headers=headers, json=payload) # Create SetDict

    assert response.json['error'] == 'Failure to create set dictionary'
    assert response.status_code == 400


def test_set_dict_toggle_complete_twice(web_client, clear_db, auth_token, spoofed_user, spoofed_empty_workout, spoof_arnold_press_dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    web_client.post('/workouts', headers=headers, json={'workout_name' : 'First Try'}) # Create Workout
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    workout_id = str(workout.id)
    payload = {
        'workout_name': spoofed_empty_workout.workout_name,
        'exercise_name': spoof_arnold_press_dict.exercise_name,
        'set_type': spoof_arnold_press_dict.set_type,
        'reps': spoof_arnold_press_dict.reps,
        'loading': spoof_arnold_press_dict.loading,
        'focus': spoof_arnold_press_dict.focus,
        'rest': spoof_arnold_press_dict.rest,
        'notes': spoof_arnold_press_dict.notes,
    }
    web_client.post(f'/workouts/{workout_id}/add_set', headers=headers, json=payload)  # Create SetDict
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    set_dict = next((set for set in workout.set_dicts_list if set.set_order == 1), None)
    set_order = set_dict.set_order

    response = web_client.patch(f'/workouts/{workout_id}/{set_order}/mark_complete', headers=headers)
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    set_dict = next((set for set in workout.set_dicts_list if set.set_order == 1), None)
    assert response.json['message'] == "Set marked complete"
    assert set_dict.complete is True

    # Second toggle (to incomplete)
    response = web_client.patch(f'/workouts/{workout_id}/{set_order}/mark_complete', headers=headers)
    spoofed_user.reload()
    workout = next((workout for workout in spoofed_user.workout_list if workout.workout_name == 'First Try'), None)
    set_dict = next((set for set in workout.set_dicts_list if set.set_order == 1), None)

    assert response.json['message'] == "Set marked incomplete"
    assert set_dict.complete is False



def test_set_dict_add_notes(web_client, auth_token, clear_db, spoofed_populated_user):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {'notes' : 'Until failure'}
    workout_id = str(spoofed_populated_user.workout_list[0].id)
    set_order = spoofed_populated_user.workout_list[0].set_dicts_list[0].set_order
    og_notes = spoofed_populated_user.workout_list[0].set_dicts_list[0].notes

    assert og_notes == 'Good form and tempo'
    response = web_client.patch(f'/workouts/{workout_id}/{set_order}/add_notes', headers=headers, json=payload)
    assert response.json['message'] == "Notes added to set"
    assert response.status_code == 201

    spoofed_populated_user.reload()
    updated_notes = spoofed_populated_user.workout_list[0].set_dicts_list[0].notes
    assert updated_notes == "Until failure"

def test_set_dict_delete_notes(web_client, auth_token, clear_db, spoofed_populated_user):
    headers = {"Authorization": f"Bearer {auth_token}"}
    workout_id = str(spoofed_populated_user.workout_list[0].id)
    set_order = spoofed_populated_user.workout_list[0].set_dicts_list[0].set_order
    og_notes = spoofed_populated_user.workout_list[0].set_dicts_list[0].notes

    assert og_notes == 'Good form and tempo'
    response = web_client.delete(f'/workouts/{workout_id}/{set_order}/delete_notes', headers=headers)
    assert response.json['message'] == "Notes deleted"
    assert response.status_code == 200

    spoofed_populated_user.reload()
    assert spoofed_populated_user.workout_list[0].set_dicts_list[0].notes == None

#TODO for SetDicts: Tests that should fail