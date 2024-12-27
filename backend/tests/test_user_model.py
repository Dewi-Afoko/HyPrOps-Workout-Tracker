import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash
from datetime import datetime

load_dotenv()

test_password = os.getenv("TEST_PASSWORD")


def test_create_user_unhashed_password():
    new_user = User(username="Test", password="unhashed_password", name="Subject", height=185, weight=175)
    assert new_user.username == "Test"
    assert new_user.password == "unhashed_password"
    assert new_user.name == "Subject"
    assert new_user.height == 185
    assert new_user.weight == 175

def test_create_user_hashed_password(user_burrito):
    assert user_burrito.username == "Chaos"
    assert check_password_hash(user_burrito.password, test_password) == True

def test_new_user_has_id_and_fixture_to_dict(user_burrito):
    assert len(str(user_burrito.id)) > 1
    assert user_burrito.to_dict() == {
        "id" : str(user_burrito.id),
        "username" : "Chaos",
        "name" : "Burrito",
        "height" : 30.0,
        "weight" : {"2024/12/27" : 35},
        "dob" : "2021/10/10"
    }

def test_update_password(user_burrito):
    user_burrito.update_password("unhashed")
    assert check_password_hash(user_burrito.password, "unhashed") == True

def test_update_some_personal_details(user_burrito):
    assert user_burrito.height == 30
    assert user_burrito.name == "Burrito"
    user_burrito.update_personal_details(height=25, name="Zan Ji")
    assert user_burrito.height == 25
    assert user_burrito.name == "Zan Ji"

def test_update_all_personal_details(user_burrito):
    user_burrito.update_personal_details(height=25, weight=30, name="Zan Ji", dob="2020/09/09")
    assert user_burrito.height == 25
    assert 30 in user_burrito.weight[-1].values()
    assert user_burrito.name == "Zan Ji"
    assert user_burrito.dob.strftime("%Y/%m/%d") == "2020/09/09"

def test_updating_details_fails_with_invalid_input(user_burrito):
    assert user_burrito.name == "Burrito"
    with pytest.raises(ValueError, match="weight must be a number"):
        user_burrito.update_personal_details(weight="Heavy")
    with pytest.raises(ValueError, match="height must be a number"):
        user_burrito.update_personal_details(height="Short")
    with pytest.raises(ValueError, match="Date of birth must be a string"):
        user_burrito.update_personal_details(dob=99)
    with pytest.raises(ValueError, match="Name must be a string"):
        user_burrito.update_personal_details(name=45.6)
    assert user_burrito.name == "Burrito"

def test_to_dict_function(user_burrito):
    assert user_burrito.to_dict() == {
        'id' : user_burrito.id,
        'username' : 'Chaos',
        'name' : 'Burrito',
        'height' : 30,
        'weight' : 35,
        'dob' : '2021/10/10'
    }