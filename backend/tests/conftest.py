import pytest
import os
import random
import sys
import py
from xprocess import ProcessStarter
from flask_jwt_extended import create_access_token
from lib.database_connection import initialize_db, close_db
from app import create_app
from models.user import User
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo
from mongoengine import connect, disconnect



@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Ensure APP_ENV is set to 'test' for the test session."""
    os.environ["APP_ENV"] = "test"


@pytest.fixture(scope="session")
def app():
    """Create a single Flask application for the test session."""
    app = create_app()
    app.config["TESTING"] = True
    initialize_db(db_name="test_db")
    yield app
    close_db()

@pytest.fixture(scope="function")
def web_client(app):
    """Provide a fresh test client for each test."""
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_database(app):
    """Clean the test database before each test."""
    with app.app_context():
        print("Cleaning database...")  # Debugging output
        for model in [User, Workout, WorkoutExerciseInfo]:
            if hasattr(model, "objects"):
                print(f"Clearing data for {model.__name__}")  # Debugging output
                model.objects.delete()


@pytest.fixture
def auth_token(app, sample_user):
    """Generate a valid JWT token for the sample_user."""
    with app.app_context():  # Use the session-scoped app fixture
        token = create_access_token(identity=sample_user.username)
        return token


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    user = User(username="testuser", password="plainpassword")  # Plain text password
    user.save()  # Password will be hashed during save()
    yield user
    user.delete()


@pytest.fixture
def sample_workout(sample_user):
    """Create a sample workout for the sample user."""
    workout = Workout(user_id=sample_user.id)
    workout.save()
    yield workout
    workout.delete()


@pytest.fixture
def sample_workout_with_exercise(sample_user):
    """Create a sample workout with an exercise for the sample user."""
    workout = Workout(user_id=sample_user.id)
    exercise_info = WorkoutExerciseInfo(
        exercise_name="Push-ups",
        reps=[10, 12],
        performance_notes=["Good form"]
    )
    workout.exercise_list.append(exercise_info)
    workout.save()
    yield workout
    workout.delete()


@pytest.fixture
def sample_user_with_workout():
    """Create a sample user with a linked workout."""
    user = User(username="testuser", password="hashedpassword")
    user.save()

    workout = Workout(user_id=user.id)
    workout.save()

    user.workout_list.append(workout)
    user.save()

    yield user
    user.delete()
    workout.delete()


@pytest.fixture(scope="session", autouse=True)
def mongo_connection():
    """Set up the MongoDB connection for the test session."""
    os.environ['APP_ENV'] = 'test'
    disconnect(alias="default")
    initialize_db(db_name="test_mongodb", alias="default")
    yield
    close_db(alias="default")


@pytest.fixture
def test_web_address(xprocess):
    """Start the test web server."""
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


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure a clean test database session."""
    disconnect(alias="default")  # Disconnect any existing connection
    initialize_db()  # Reconnect to the appropriate database based on APP_ENV
    yield
    disconnect(alias="default")  # Cleanly disconnect after tests

@pytest.fixture
def empty_auth_token(app):
    """Generate a valid JWT token for a non-existent user."""
    with app.app_context():
        token = create_access_token(identity="nonexistent_user")
        return token
