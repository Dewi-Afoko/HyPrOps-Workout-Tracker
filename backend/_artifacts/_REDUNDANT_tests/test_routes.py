import pytest
from mongoengine.errors import NotUniqueError
from models.user import User
from models.workout import Workout
from flask_jwt_extended import create_access_token
from bson import ObjectId
from werkzeug.security import generate_password_hash


def test_create_user_success(web_client, clean_database):
    """Test creating a new user successfully."""
    data = {"username": "testuser", "password": "password123"}
    response = web_client.post('/users', json=data)

    assert response.status_code == 201
    response_data = response.get_json()
    assert "id" in response_data
    assert response_data["username"] == data["username"]

    # Verify user is saved in the database
    user_in_db = User.objects(username=data["username"]).first()
    assert user_in_db is not None
    assert user_in_db.username == data["username"]


def test_create_user_duplicate_error(web_client, clean_database):
    """Test creating a user with an already existing username."""
    # Create the first user
    User(username="testuser", password="password123").save()

    # Attempt to create the same user again
    data = {"username": "testuser", "password": "password123"}
    response = web_client.post('/users', json=data)

    assert response.status_code == 400
    assert response.get_json() == {"error": "Username already exists"}


def test_get_users_success(web_client, auth_token, sample_user):
    """Test retrieving users successfully."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = web_client.get('/users', headers=headers)

    assert response.status_code == 200
    response_data = response.get_json()
    assert "users" in response_data
    assert len(response_data["users"]) == 1
    assert response_data["users"][0]["username"] == sample_user.username


def test_get_users_empty_database(web_client, empty_auth_token, clean_database):
    """Test retrieving users when the database is empty."""
    headers = {"Authorization": f"Bearer {empty_auth_token}"}

    # Debug: Verify database state before the test
    users_in_db = User.objects()
    print(f"Users in database before test: {len(users_in_db)}")  # Debugging output

    response = web_client.get('/users', headers=headers)

    print(f"Response JSON: {response.get_json()}")  # Debugging output

    assert response.status_code == 400
    assert response.get_json() == {"error": "No users found!"}


def test_get_users_unauthorized(web_client):
    """Test retrieving users without a valid token."""
    response = web_client.get('/users')

    assert response.status_code == 401
    assert response.get_json() == {"msg": "Missing Authorization Header"}

def test_create_workout_exercise_success(web_client, auth_token, sample_workout):
    """Test adding an exercise to a workout successfully."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups"}
    response = web_client.post(
        f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/add_exercise",
        headers=headers,
        json=data
    )

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["workout id"] == str(sample_workout.id)
    assert response_data["exercise added"] == "Push-ups"

    # Verify the exercise was added to the workout
    workout_in_db = Workout.objects(id=sample_workout.id).first()
    assert len(workout_in_db.exercise_list) == 1
    assert workout_in_db.exercise_list[0].exercise_name == "Push-ups"



def test_create_workout_exercise_duplicate(web_client, auth_token, sample_workout_with_exercise):
    """Test adding a duplicate exercise to a workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups"}
    response = web_client.post(
        f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/add_exercise",
        headers=headers,
        json=data
    )

    assert response.status_code == 418
    assert response.get_json() == {"error": "Exercise already exists, try adding details!"}



def test_create_workout_exercise_workout_not_found(web_client, auth_token):
    """Test adding an exercise to a non-existent workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups"}
    response = web_client.post(
        f"/workouts/{ObjectId()}/{ObjectId()}/add_exercise",
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}



def test_add_details_to_exercise_success(web_client, auth_token, sample_workout_with_exercise):
    """Test adding details to an existing exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups", "reps": 15, "loading": 50, "rest": 60, "notes": "Felt great"}
    response = web_client.patch(
        f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/add_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data == {
        "reps": 15,
        "loading": 50,
        "rest": 60,
        "notes": "Felt great"
    }



def test_add_details_exercise_not_found(web_client, auth_token, sample_workout):
    """Test adding details to a non-existent exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Non-existent", "reps": 10}
    response = web_client.patch(
        f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/add_details",  # Use `sample_workout.user_id.id`
        headers=headers,
        json=data
    )

    assert response.status_code == 418
    assert response.get_json() == {"error": "Exercise not found!"}



def test_add_details_workout_not_found(web_client, auth_token):
    """Test adding details to an exercise in a non-existent workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups", "reps": 10}
    response = web_client.patch(
        f"/workouts/{ObjectId()}/{ObjectId()}/add_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}


def test_edit_details_success(web_client, auth_token, sample_workout_with_exercise):
    """Test editing details of an existing exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "exercise_name": "Push-ups",
        "reps_index": 0,
        "reps_value": 15,
        "performance_notes_index": 0,
        "performance_notes_value": "Improved form"
    }
    response = web_client.patch(
        f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/edit_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == {
        "updated_reps": "reps[0] = 15",
        "updated_performance_notes": "performance_notes[0] = Improved form"
    }


def test_edit_details_exercise_not_found(web_client, auth_token, sample_workout):
    """Test editing details for a non-existent exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Non-existent", "reps_index": 0, "reps_value": 15}
    response = web_client.patch(
        f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/edit_details",  # Use `sample_workout.user_id.id`
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Exercise not found"}



def test_edit_details_workout_not_found(web_client, auth_token):
    """Test editing details of an exercise in a non-existent workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups", "reps_index": 0, "reps_value": 15}
    response = web_client.patch(
        f"/workouts/{ObjectId()}/{ObjectId()}/edit_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}

def test_create_workout_exercise_success(web_client, auth_token, sample_workout):
    """Test adding an exercise to a workout successfully."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups"}

    response = web_client.post(
        f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/add_exercise",  # Use `user_id.id` as ObjectId
        headers=headers,
        json=data
    )

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["workout id"] == str(sample_workout.id)
    assert response_data["exercise added"] == "Push-ups"

    # Verify the database state
    updated_workout = Workout.objects(id=sample_workout.id).first()
    assert len(updated_workout.exercise_list) == 1
    assert updated_workout.exercise_list[0].exercise_name == "Push-ups"



def test_create_workout_exercise_duplicate(web_client, auth_token, sample_workout_with_exercise):
    """Test adding a duplicate exercise to a workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups"}

    response = web_client.post(
        f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/add_exercise",
        headers=headers,
        json=data
    )

    assert response.status_code == 418
    assert response.get_json() == {"error": "Exercise already exists, try adding details!"}



def test_create_workout_exercise_workout_not_found(web_client, auth_token):
    """Test adding an exercise to a non-existent workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups"}
    response = web_client.post(
        f"/workouts/{ObjectId()}/{ObjectId()}/add_exercise",
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}


def test_add_details_to_exercise_success(web_client, auth_token, sample_workout_with_exercise):
    """Test adding details to an existing exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups", "reps": 10, "loading": 50, "rest": 60, "notes": "Felt good"}

    response = web_client.patch(
        f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/add_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data == {
        "reps": 10,
        "loading": 50,
        "rest": 60,
        "notes": "Felt good"
    }

    # Verify the database state
    updated_workout = Workout.objects(id=sample_workout_with_exercise.id).first()
    assert updated_workout.exercise_list[0].reps[-1] == 10  # Verify the last added rep



def test_add_details_exercise_not_found(web_client, auth_token, sample_workout):
    """Test adding details to a non-existent exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Non-existent", "reps": 10}
    response = web_client.patch(
        f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/add_details",  # Use `sample_workout.user_id.id`
        headers=headers,
        json=data
    )

    assert response.status_code == 418
    assert response.get_json() == {"error": "Exercise not found!"}



def test_add_details_workout_not_found(web_client, auth_token):
    """Test adding details to an exercise in a non-existent workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups", "reps": 10}
    response = web_client.patch(
        f"/workouts/{ObjectId()}/{ObjectId()}/add_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}


def test_edit_details_success(web_client, auth_token, sample_workout_with_exercise):
    """Test editing details of an existing exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "exercise_name": "Push-ups",
        "reps_index": 0,
        "reps_value": 15,
        "performance_notes_index": 0,
        "performance_notes_value": "Improved form"
    }

    response = web_client.patch(
        f"/workouts/{sample_workout_with_exercise.user_id.id}/{sample_workout_with_exercise.id}/edit_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == {
        "updated_reps": "reps[0] = 15",
        "updated_performance_notes": "performance_notes[0] = Improved form"
    }

    # Verify the database state
    updated_workout = Workout.objects(id=sample_workout_with_exercise.id).first()
    assert updated_workout.exercise_list[0].reps[0] == 15
    assert updated_workout.exercise_list[0].performance_notes[0] == "Improved form"



def test_edit_details_exercise_not_found(web_client, auth_token, sample_workout):
    """Test editing details for a non-existent exercise."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Non-existent", "reps_index": 0, "reps_value": 15}
    response = web_client.patch(
        f"/workouts/{sample_workout.user_id.id}/{sample_workout.id}/edit_details",  # Use `sample_workout.user_id.id`
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Exercise not found"}


def test_edit_details_workout_not_found(web_client, auth_token):
    """Test editing details of an exercise in a non-existent workout."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"exercise_name": "Push-ups", "reps_index": 0, "reps_value": 15}
    response = web_client.patch(
        f"/workouts/{ObjectId()}/{ObjectId()}/edit_details",
        headers=headers,
        json=data
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found"}

def test_login_success(web_client, clean_database):
    """Test logging in with valid credentials."""
    # Create a user
    username = "testuser"
    password = "password123"
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    user.save()

    # Login request
    data = {"username": username, "password": password}
    response = web_client.post('/token/login', json=data)

    assert response.status_code == 200
    response_data = response.get_json()
    assert "token" in response_data
    assert response_data["advice"] == "It's dangerous to go alone, take this with you *hands over a JWT*"


def test_login_invalid_username(web_client, clean_database):
    """Test logging in with an invalid username."""
    # Login request with non-existent username
    data = {"username": "invaliduser", "password": "password123"}
    response = web_client.post('/token/login', json=data)

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid username or password"}


def test_login_invalid_password(web_client, clean_database):
    """Test logging in with an invalid password."""
    # Create a user
    username = "testuser"
    password = "password123"
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    user.save()

    # Login request with incorrect password
    data = {"username": username, "password": "wrongpassword"}
    response = web_client.post('/token/login', json=data)

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid username or password"}


def test_login_missing_fields(web_client):
    """Test logging in with missing fields."""
    data = {"username": "testuser"}  # Missing password
    response = web_client.post('/token/login', json=data)

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid username or password"}


def test_token_check_success(web_client, auth_token):
    """Test token validation with a valid JWT."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = web_client.get('/token/token_check', headers=headers)

    assert response.status_code == 200
    response_data = response.get_json()
    assert "Welcome, user" in response_data["message"]
    assert response_data["advice"] == "It's dangerous to go alone, take this with you *hands over a JWT*"


def test_token_check_missing_token(web_client):
    """Test token validation without a JWT."""
    response = web_client.get('/token/token_check')

    assert response.status_code == 401
    assert "msg" in response.get_json()
    assert response.get_json()["msg"] == "Missing Authorization Header"


def test_token_check_invalid_token(web_client):
    """Test token validation with an invalid JWT."""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = web_client.get('/token/token_check', headers=headers)

    assert response.status_code == 422  # Expecting 422 for malformed tokens
    assert "msg" in response.get_json()
    assert response.get_json()["msg"] == "Not enough segments"  # This is the common error for malformed tokens
