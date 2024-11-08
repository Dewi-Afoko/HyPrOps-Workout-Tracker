import pytest
import sys
import random
import py
import os
from xprocess import ProcessStarter
from mongoengine import connect, disconnect
from lib.database_connection import initialize_db, close_db
from app import create_app 
from models.user import User
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo

# Fixture for MongoDB connection
@pytest.fixture(scope="session", autouse=True)
def mongo_connection():
    # Set environment to 'test' for safe test database usage
    os.environ['APP_ENV'] = 'test'
    
    # Disconnect any active connections and connect to the test database
    disconnect(alias="default")
    initialize_db(db_name="test_mongodb", alias="default")  # Ensure this is a dedicated test database
    yield
    close_db(alias="default")

# Fixture for starting the test server
@pytest.fixture
def test_web_address(xprocess):
    python_executable = sys.executable
    app_file = py.path.local(__file__).dirpath("../app.py")
    port = str(random.randint(4000, 4999))
    
    class Starter(ProcessStarter):
        env = {"PORT": port, "APP_ENV": "test", **os.environ}
        pattern = "Debugger PIN"
        args = [python_executable, app_file]

    xprocess.ensure("flask_test_server", Starter)

    yield f"localhost:{port}"

    xprocess.getinfo("flask_test_server").terminate()

# Fixture for creating a Flask test client
@pytest.fixture
def web_client():
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode

    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_user():
    user = User(username="testuser", password="hashedpassword")
    user.save()
    yield user
    user.delete()  # Cleanup after test

@pytest.fixture
def sample_workout(sample_user):
    workout = Workout(user_id=sample_user.id)
    workout.save()
    yield workout
    workout.delete()

@pytest.fixture
def sample_workout_with_exercise(sample_user):
    # Create a Workout and add an exercise to its exercise_list
    workout = Workout(user_id=sample_user.id)
    exercise_info = WorkoutExerciseInfo(exercise_name="Push-ups", reps=[10, 12])
    workout.exercise_list.append(exercise_info)
    workout.save()
    yield workout
    workout.delete()

@pytest.fixture
def sample_user_with_workout():
    # Create a User instance
    user = User(username="testuser", password="hashedpassword")
    user.save()  # Save the user first to generate an id

    # Create and save a Workout instance, linking it to the user
    workout = Workout(user_id=user.id)
    workout.save()  # Save workout first before adding to workout_list

    # Add the saved workout to the user's workout_list
    user.workout_list.append(workout)
    user.save()  # Save the user again with the workout reference

    yield user
    user.delete()  # Cleanup after test
    workout.delete()

@pytest.fixture(autouse=True)
def clean_database():
    yield
    for model in [User, Workout, WorkoutExerciseInfo]:
        if hasattr(model, 'objects'):
            model.objects.delete()