import pytest
from models.user import User
from models.workout import Workout
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError


def test_create_user(sample_user):
    assert sample_user.username == "testuser"
    assert sample_user.password == "hashedpassword"
    assert sample_user.workout_list == []  # Ensure no workouts initially


def test_update_password(sample_user):
    sample_user.update_password("newhashedpassword")
    sample_user.save()
    updated_user = User.objects(id=sample_user.id).first()
    assert updated_user.password == "newhashedpassword"

def test_add_workout(sample_user):
    workout = Workout(user_id=sample_user.id)
    workout.save()

    sample_user.add_workout(workout)
    sample_user.save()
    
    updated_user = User.objects(id=sample_user.id).first()
    assert len(updated_user.workout_list) == 1
    assert updated_user.workout_list[0].id == workout.id

def test_duplicate_username(sample_user):
    with pytest.raises(NotUniqueError):
        duplicate_user = User(username="testuser", password="anotherpassword")
        duplicate_user.save()

def test_create_user_without_username():
    with pytest.raises(ValidationError):
        user = User(password="hashedpassword")
        user.save()
        
def test_user_equality(sample_user):
    user_copy = User.objects(id=sample_user.id).first()
    assert sample_user == user_copy

def test_user_repr(sample_user_with_workout):
    # Expected __repr__ output
    expected_repr = f"User(username={sample_user_with_workout.username}, workout_list={sample_user_with_workout.workout_list})"
    assert repr(sample_user_with_workout) == expected_repr

def test_user_id_initialization():
    # Create a User without saving, so id should be None
    user = User(username="new_user", password="newpassword")
    
    # Ensure id is None until the user is saved
    if not hasattr(user, 'id'):
        user.id = None

    expected_repr = f"User(username={user.username}, workout_list={user.workout_list})"
    assert repr(user) == expected_repr
    assert user.id is None  # Confirm id is None until saved

def test_user_id_initialization_before_save():
    # Create a User instance without saving
    user = User(username="unsaved_user", password="password")
    
    # Verify that id is set to None (due to `__init__` logic)
    assert user.id is None

def test_user_id_initialization_after_save():
    # Create and save a User instance
    user = User(username="saved_user", password="password")
    user.save()  # Save the user to generate an `_id`

    # Fetch the saved user from the database to ensure `id` is set correctly
    saved_user = User.objects(id=user.id).first()
    assert saved_user.id == user.id  # Verify `id` is now set to MongoDB's `_id`

    # Cleanup
    user.delete()