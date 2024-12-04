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

def test_toggling_workout_complete(spoofed_empty_workout):
    spoofed_empty_workout.toggle_complete()
    assert spoofed_empty_workout.complete == True

def test_toggling_workout_complete_twice(spoofed_empty_workout):
    spoofed_empty_workout.toggle_complete()
    assert spoofed_empty_workout.complete == True
    spoofed_empty_workout.toggle_complete()
    assert spoofed_empty_workout.complete == False

def test_adding_sets_dicts(spoofed_empty_workout):
    set_dict = SetDicts(exercise_name="Bench Press")
    spoofed_empty_workout.add_set_dict(set_dict)
    assert spoofed_empty_workout.set_dicts_list == [set_dict]

def test_adding_user_stats(spoofed_empty_workout, spoofed_personal_data):
    stats = UserStats(weight=spoofed_personal_data, sleep_score=80, sleep_quality="Good!", notes="Feeling it today!")
    # stats.set_weight()
    spoofed_empty_workout.add_stats(stats)
    assert spoofed_empty_workout.user_stats == stats
    assert spoofed_empty_workout.user_stats.weight.weight == 25
    stats.set_weight()
    assert stats.weight == 25

def test_add_workout_notes(spoofed_empty_workout):
    note = "Feel pretty good..."
    spoofed_empty_workout.add_notes(note)
    assert spoofed_empty_workout.notes == ["Feel pretty good..."]