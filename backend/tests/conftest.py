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
from models.set_dicts import SetDicts
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
    Workout.objects.delete()


@pytest.fixture
def user_burrito(testing_password):
    burrito = User(username="Chaos", password=testing_password, name="Burrito", height=30, weight=[{"2024/12/27" : 35}], dob=datetime.strptime("2021/10/10", "%Y/%m/%d"))
    burrito.hash_password()
    burrito.save()
    yield burrito

@pytest.fixture
def auth_token(user_burrito):
    token = create_access_token(str(user_burrito.username))
    yield token
