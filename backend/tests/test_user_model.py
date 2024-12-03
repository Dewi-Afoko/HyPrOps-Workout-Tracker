import pytest
from models.user import User
from models.workout import Workout
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash

def test_create_user_unhashed_password():
    new_user = User(username="Test", _password="unhashed_password")
    assert new_user.username == "Test"
    assert new_user._password == "unhashed_password"
