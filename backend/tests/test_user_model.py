import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash

load_dotenv()

test_password = os.getenv("TEST_PASSWORD")


def test_create_user_unhashed_password():
    new_user = User(username="Test", password="unhashed_password")
    assert new_user.username == "Test"
    assert new_user.password == "unhashed_password"

def test_create_user_hashed_password(spoofed_user):
    assert spoofed_user.username == "Test"
    assert check_password_hash(spoofed_user.password, test_password) == True

def test_new_user_has_id(spoofed_user):
    assert len(str(spoofed_user.id)) > 1

def test_adding_workout_to_list(spoofed_user, spoofed_empty_workout):
    spoofed_user.add_workout(spoofed_empty_workout.id)
    assert spoofed_user.workout_list == [spoofed_empty_workout.id]

def test_adding_personal_data(spoofed_user, spoofed_personal_data):
    spoofed_user.add_personal_data(spoofed_personal_data)
    assert spoofed_user.personal_data == spoofed_personal_data

def test_to_dict_with_all_properties(spoofed_user, spoofed_personal_data, spoofed_empty_workout):
    spoofed_user.add_personal_data(spoofed_personal_data)
    spoofed_user.add_workout(spoofed_empty_workout)
    assert spoofed_user.to_dict() == {
            'id' : str(spoofed_user.id),
            'username' : spoofed_user.username,
            'workout_list' : spoofed_user.workout_list,
            'personal_data' : str(spoofed_user.personal_data),
        }

def test_update_password(spoofed_user):
    spoofed_user.update_password('newPassWord')
    assert check_password_hash(spoofed_user.password, 'newPassWord') == True

def test_delete_workout(spoofed_user, spoofed_empty_workout):
    spoofed_user.add_workout(spoofed_empty_workout.id)
    spoofed_user.add_workout(spoofed_empty_workout.id)
    assert spoofed_user.workout_list == [spoofed_empty_workout.id, spoofed_empty_workout.id]
    spoofed_user.delete_workout(spoofed_empty_workout.id)
    assert spoofed_user.workout_list == [spoofed_empty_workout.id]

def test_deleting_personal_data(spoofed_user, spoofed_personal_data):
    spoofed_user.add_personal_data(spoofed_personal_data)
    assert spoofed_user.personal_data == spoofed_personal_data
    spoofed_user.delete_personal_data()
    assert spoofed_user.personal_data == None