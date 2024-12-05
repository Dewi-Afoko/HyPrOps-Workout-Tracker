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

def test_adding_sets_dict_object(spoofed_empty_workout, spoof_arnold_press_dict):
    spoofed_empty_workout.add_set_dict(spoof_arnold_press_dict)
    assert spoofed_empty_workout.set_dicts_list == [spoof_arnold_press_dict]

def test_adding_sets_dict_object_twice(spoofed_empty_workout, spoof_arnold_press_dict):
    set_dict = SetDicts(set_order=1, exercise_name="Arnold Press", set_number=1, set_type="Warm up", reps=12, loading=13.5, focus="Form", rest=60, notes="Shoulder warm up")
    spoofed_empty_workout.add_set_dict(spoof_arnold_press_dict)
    spoofed_empty_workout.add_set_dict(set_dict)
    assert spoofed_empty_workout.set_dicts_list == [spoof_arnold_press_dict, set_dict]

def test_to_dict_method(spoofed_empty_workout, spoofed_user_stats, spoof_arnold_press_dict):
    spoofed_empty_workout.add_stats(spoofed_user_stats)
    spoofed_empty_workout.add_set_dict(spoof_arnold_press_dict)
    assert spoofed_empty_workout.to_dict() == {
            "id": str(spoofed_empty_workout.id),
            "user_id": str(spoofed_empty_workout.user_id.id),
            "workout_name": spoofed_empty_workout.workout_name,
            "date": spoofed_empty_workout.date,
            "complete": spoofed_empty_workout.complete,
            "sets_dict_list": [spoof_arnold_press_dict],
            "user_stats": spoofed_empty_workout.user_stats,
            "notes": spoofed_empty_workout.notes,
        }
    
def test_delete_set_dict(spoofed_empty_workout, spoof_arnold_press_dict):
    spoofed_empty_workout.add_set_dict(spoof_arnold_press_dict)
    spoofed_empty_workout.add_set_dict(spoof_arnold_press_dict)
    assert spoofed_empty_workout.set_dicts_list == [spoof_arnold_press_dict, spoof_arnold_press_dict]
    spoofed_empty_workout.delete_set_dict(spoof_arnold_press_dict)
    assert spoofed_empty_workout.set_dicts_list == [spoof_arnold_press_dict]

def test_delete_workout_notes(spoofed_empty_workout):
    note_1 = "Feel pretty good..."
    note_2 = "Feel pretty mid..."
    note_3 = "Feel pretty bad..."
    spoofed_empty_workout.add_notes(note_1)
    spoofed_empty_workout.add_notes(note_2)
    spoofed_empty_workout.add_notes(note_3)
    spoofed_empty_workout.delete_note(0)
    spoofed_empty_workout.delete_note(-1)
    assert spoofed_empty_workout.notes == ["Feel pretty mid..."]