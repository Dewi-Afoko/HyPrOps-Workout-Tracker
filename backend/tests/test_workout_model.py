import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from models.set_dicts import SetDicts
from models.user_stats import UserStats
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError

def test_workout_creation_generates_correctly(spoofed_user):
    new_workout = Workout(user_id=spoofed_user.id, workout_name="First Try")
    spoofed_user.save()
    assert new_workout.workout_name == "First Try"
    assert bool(new_workout.user_id) == True
    assert new_workout.complete == False
    assert len(new_workout.set_dicts_list) == 0
    assert bool(new_workout.user_stats) == False
    assert len(new_workout.notes) == 0
