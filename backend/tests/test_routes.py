import pytest
from mongoengine.errors import NotUniqueError
from models import User
from bson import ObjectId
import json
from flask_jwt_extended import create_access_token


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


### Route: edit_details_in_exercise_info (PATCH /workouts/<user_id>/<workout_id>/edit_details)

def test_edit_details_success(web_client, sample_workout_with_exercise):
    workout_id = str(sample_workout_with_exercise.id)
    user_id = str(sample_workout_with_exercise.user_id.id)  # Access `id` of the `user_id` object
    url = f"/workouts/{user_id}/{workout_id}/edit_details"

    # Data for updating reps and performance notes for an existing exercise
    data = {
        "exercise_name": "Push-ups",
        "reps_index": 1,
        "reps_value": 15,
        "performance_notes_index": 0,
        "performance_notes_value": "Improved form"
    }

    # Send the PATCH request
    response = web_client.patch(url, json=data)

    # Check response and verify updates
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == {
        "updated_reps": "reps[1] = 15",
        "updated_performance_notes": "performance_notes[0] = Improved form"
    }


def test_edit_details_workout_not_found(web_client):
    # Generate valid but non-existent ObjectIds
    fake_user_id = str(ObjectId())
    fake_workout_id = str(ObjectId())
    url = f"/workouts/{fake_user_id}/{fake_workout_id}/edit_details"

    # Data for attempting an update
    data = {
        "exercise_name": "Push-ups",
        "reps_index": 1,
        "reps_value": 15
    }

    # Send the PATCH request
    response = web_client.patch(url, json=data)

    # Assert the response for a missing workout
    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}


def test_edit_details_exercise_not_found(web_client, sample_workout_with_exercise):
    workout_id = str(sample_workout_with_exercise.id)
    user_id = str(sample_workout_with_exercise.user_id.id)  # Access `id` of the `user_id` object
    url = f"/workouts/{user_id}/{workout_id}/edit_details"

    # Data with a non-existent exercise name
    data = {
        "exercise_name": "Squats",  # This exercise is not in the workout
        "reps_index": 1,
        "reps_value": 15
    }

    # Send the PATCH request
    response = web_client.patch(url, json=data)

    # Assert the response for a missing exercise
    assert response.status_code == 404
    assert response.get_json() == {"error": "Exercise not found"}


def test_edit_details_no_updates_provided(web_client, sample_workout_with_exercise):
    workout_id = str(sample_workout_with_exercise.id)
    user_id = str(sample_workout_with_exercise.user_id.id)  # Access `id` of the `user_id` object
    url = f"/workouts/{user_id}/{workout_id}/edit_details"

    # Data only contains the exercise name, no update fields
    data = {
        "exercise_name": "Push-ups"
    }

    # Send the PATCH request
    response = web_client.patch(url, json=data)

    # Assert the response indicating no updates were provided
    assert response.status_code == 400
    assert response.get_json() == {"message": "No details to update provided or indices out of range"}

def test_login_success(web_client, sample_user):
    """Test successful login with valid credentials."""
    response = web_client.post(
        "/token/login",
        json={"username": "testuser", "password": "plainpassword"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert "advice" in data
    assert data["advice"] == "It's dangerous to go alone, take this with you *hands over a *JWT*"


def test_login_failure_invalid_username(web_client):
    """Test login failure with invalid username."""
    response = web_client.post(
        "/token/login",
        json={"username": "wronguser", "password": "plainpassword"},
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid username or password"


def test_login_failure_invalid_password(web_client, sample_user):
    """Test login failure with invalid password."""
    response = web_client.post(
        "/token/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid username or password"


def test_token_check_success(web_client, sample_user):
    """Test successful access to token_check with valid JWT."""
    # Generate a JWT for the test user
    with web_client.application.app_context():
        access_token = create_access_token(identity=str(sample_user.id))

    headers = {"Authorization": f"Bearer {access_token}"}
    response = web_client.get("/token/token_check", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "advice" in data
    assert f"Welcome, user {sample_user.id}!" in data["message"]
    assert data["advice"] == "It's dangerous to go alone, take this with you *hands over a *JWT*"


def test_token_check_failure_missing_token(web_client):
    """Test access to token_check without a JWT."""
    response = web_client.get("/token/token_check")
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"


def test_token_check_failure_invalid_token(web_client):
    """Test access to token_check with an invalid JWT."""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = web_client.get("/token/token_check", headers=headers)
    assert response.status_code == 422
    data = response.get_json()
    assert data["msg"] == "Not enough segments"