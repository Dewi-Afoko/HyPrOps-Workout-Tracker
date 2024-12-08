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
from models.user_stats import UserStats
from models.set_dicts import SetDicts
from models.personal_data import PersonalData
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

test_password = os.getenv("TEST_PASSWORD")

@pytest.fixture
def testing_password():
    test_password = os.getenv("TEST_PASSWORD")
    return test_password


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


@pytest.fixture
def auth_token(app, sample_user):
    """Generate a valid JWT token for the sample_user."""
    with app.app_context():  # Use the session-scoped app fixture
        token = create_access_token(identity=sample_user.username)
        return token


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


@pytest.fixture(autouse=True)
def clear_db():
    User.objects.delete()


@pytest.fixture
def spoofed_user():
    spoofed_user = User(username="Test", password=test_password)
    spoofed_user.hash_password()
    spoofed_user.save()
    yield spoofed_user

@pytest.fixture
def spoofed_empty_workout(spoofed_user):
    new_workout = Workout(user_id=spoofed_user.id, workout_name="First Try")
    spoofed_user.save()
    yield new_workout

@pytest.fixture
def spoofed_personal_data():
    new_data = PersonalData(name="Burrito", dob=datetime(2021, 11, 12), height=25, weight=25)
    yield new_data

@pytest.fixture
def spoofed_personal_data_2():
    new_data = PersonalData(name="Burrito", dob=datetime(2021, 11, 12), height=25, weight=250)
    yield new_data

@pytest.fixture
def spoofed_user_stats(spoofed_personal_data):
        stats = UserStats(weight=spoofed_personal_data, sleep_score=80, sleep_quality="Great", notes="Ready to start!")
        yield stats

@pytest.fixture
def spoof_arnold_press_dict():
        set_dict = SetDicts(set_order=1, exercise_name="Arnold Press", set_number=1, set_type="Working", reps=10, loading=20, focus="Form", rest=60, notes="Good form and tempo")
        yield set_dict

@pytest.fixture
def auth_token(spoofed_user):
    access_token = create_access_token(identity=spoofed_user.username)
    yield access_token


@pytest.fixture
def bad_token():
    access_token = create_access_token(identity="Invalid")
    yield access_token
