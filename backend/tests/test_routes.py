import pytest
from mongoengine.errors import NotUniqueError
from models import User
from bson import ObjectId


def test_home_route(web_client):
    response = web_client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to HyPrOps backend... We finna be cooking!!"}

def test_creating_user(web_client):
    data = {"username": "TestOnev",
            "password": "1234"}
    
    response = web_client.post('/users', json=data)
    assert response.status_code == 201
    
def test_duplicate_user_error(web_client):
    data = {"username": "TestOnev",
            "password": "1234"}
    
    response = web_client.post('/users', json=data)
    assert response.status_code == 201 

    # Second request with the same username to trigger the duplicate error
    response = web_client.post('/users', json=data)
    assert response.status_code == 400 
    assert response.json == {"error": "Username already exists"}  

def test_returning_user(web_client):
    data = {"username": "TestOnev",
            "password": "1234"}
    
    creation = web_client.post('/users', json=data)
    assert creation.status_code == 201
    response = web_client.get('/users')
    assert response.status_code == 200

def test_get_with_no_users(web_client):
    response = web_client.get('/users')
    assert response.status_code == 400
    assert response.json == {'error': 'No users found!'}

### Route: my_workouts (GET /workouts/<user_id>)

def test_get_my_workouts_success(web_client, sample_user_with_workout):
    response = web_client.get(f"/workouts/{sample_user_with_workout.id}")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0  # Confirm at least one workout is returned

def test_get_my_workouts_user_not_found(web_client):
    response = web_client.get("/workouts/60b7a57f4f1d2c3a2d123456")  # Non-existent user ID
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

### Route: create_workout (POST /workouts/<user_id>)

def test_create_workout_success(web_client, sample_user):
    response = web_client.post(f"/workouts/{sample_user.id}")
    assert response.status_code == 201
    assert "user_id" in response.json
    assert "workout_id" in response.json

def test_create_workout_user_not_found(web_client):
    response = web_client.post("/workouts/60b7a57f4f1d2c3a2d123456")  # Non-existent user ID
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

### Route: create_workout_exercise_info (POST /workouts/<user_id>/<workout_id>/add_exercise)

def test_create_workout_exercise_success(web_client, sample_workout):
    data = {"exercise_name": "Squat"}
    response = web_client.post(f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/add_exercise", json=data)
    assert response.status_code == 201
    assert response.json["exercise added"] == "Squat"

def test_create_workout_exercise_duplicate(web_client, sample_workout_with_exercise):
    data = {"exercise_name": "Push-ups"}  # Duplicate exercise name
    response = web_client.post(f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/add_exercise", json=data)
    assert response.status_code == 418
    assert response.json == {"error": "Exercise already exists, try adding details!"}

def test_create_workout_exercise_workout_not_found(web_client, sample_user):
    data = {"exercise_name": "Lunge"}
    response = web_client.post(f"/workouts/{sample_user.id}/60b7a57f4f1d2c3a2d123456/add_exercise", json=data)
    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}

### Route: add_details_to_exercise_info (PATCH /workouts/<user_id>/<workout_id>/add_details)

def test_add_details_to_exercise_success(web_client, sample_workout_with_exercise):
    data = {
        "exercise_name": "Push-ups",
        "reps": 15,
        "loading": 20,
        "rest": 30,
        "notes": "Felt strong"
    }
    response = web_client.patch(f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/add_details", json=data)
    assert response.status_code == 201
    assert response.json == {
        "reps": 15,
        "loading": 20,
        "rest": 30,
        "notes": "Felt strong"
    }

def test_add_details_exercise_not_found(web_client, sample_workout):
    data = {
        "exercise_name": "Nonexistent Exercise",
        "reps": 10
    }
    response = web_client.patch(f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/add_details", json=data)
    assert response.status_code == 418
    assert response.json == {"error": "Exercise not found!"}

def test_add_details_workout_not_found(web_client, sample_user):
    data = {"exercise_name": "Push-ups", "reps": 10}
    response = web_client.patch(f"/workouts/{sample_user.id}/60b7a57f4f1d2c3a2d123456/add_details", json=data)
    assert response.status_code == 404
    assert response.json == {"error": "Workout not found"}