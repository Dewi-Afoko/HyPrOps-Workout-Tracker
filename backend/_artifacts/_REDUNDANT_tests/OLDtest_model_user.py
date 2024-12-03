import pytest
from models.user import User
from models.workout import Workout
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash


def test_create_user(sample_user):
    assert sample_user.username == "testuser"
    # Verify the hashed password matches the plain password
    assert check_password_hash(sample_user.password, "plainpassword")  # Match with original plain password
    assert sample_user.workout_list == []  # Ensure no workouts initially



def test_update_password(sample_user):
    # Update the password
    sample_user.update_password("newpassword")
    sample_user.save()

    # Fetch the updated user from the database
    updated_user = User.objects(id=sample_user.id).first()

    # Verify the hashed password matches the new password
    assert check_password_hash(updated_user.password, "newpassword")





def test_add_workout(sample_user, sample_workout):
    # Add workout to the user
    sample_user.add_workout(sample_workout)
    sample_user.save()

    # Fetch the updated user from the database
    updated_user = User.objects(id=sample_user.id).first()

    # Verify the workout is added
    assert len(updated_user.workout_list) == 1
    assert updated_user.workout_list[0].id == sample_workout.id


def test_duplicate_username(sample_user):
    # Attempt to create another user with the same username
    with pytest.raises(NotUniqueError):
        duplicate_user = User(username="testuser", password="anotherpassword")
        duplicate_user.save()


def test_create_user_without_username():
    # Attempt to create a user without a username
    with pytest.raises(ValidationError):
        user = User(password="password")
        user.save()


def test_user_equality(sample_user):
    # Fetch the user from the database
    user_copy = User.objects(id=sample_user.id).first()
    # Assert equality
    assert sample_user == user_copy


def test_user_repr(sample_user_with_workout):
    # Expected `__repr__` output
    expected_repr = f"User(username={sample_user_with_workout.username}, workout_list={sample_user_with_workout.workout_list})"
    assert repr(sample_user_with_workout) == expected_repr


def test_user_id_initialization():
    # Create a User without saving, so id should be None
    user = User(username="new_user", password="newpassword")

    # Verify id is None
    assert user.id is None

    # Expected `__repr__` output
    expected_repr = f"User(username={user.username}, workout_list={user.workout_list})"
    assert repr(user) == expected_repr


def test_user_id_initialization_after_save():
    # Create and save a User instance
    user = User(username="saved_user", password="password")
    user.save()  # Save the user to generate an `_id`

    # Fetch the saved user from the database
    saved_user = User.objects(id=user.id).first()

    # Verify the id is set correctly
    assert saved_user.id == user.id

    # Cleanup
    user.delete()


def test_user_with_workout(sample_user_with_workout):
    # Fetch the user with a workout
    user = User.objects(id=sample_user_with_workout.id).first()

    # Verify the user has a workout in their workout_list
    assert len(user.workout_list) == 1
    assert user.workout_list[0].id == sample_user_with_workout.workout_list[0].id


def test_workout_with_exercise(sample_workout_with_exercise):
    # Fetch the workout with exercises
    workout = Workout.objects(id=sample_workout_with_exercise.id).first()

    # Verify the workout has exercises
    assert len(workout.exercise_list) == 1
    assert workout.exercise_list[0].exercise_name == "Push-ups"
    assert workout.exercise_list[0].reps == [10, 12]
    assert workout.exercise_list[0].performance_notes == ["Good form"]
