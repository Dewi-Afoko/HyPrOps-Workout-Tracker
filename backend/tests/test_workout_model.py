import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from models.set_dicts import SetDicts
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError

def test_workout_creation_generates_correctly(user_burrito):
    new_workout = Workout(user_id=user_burrito.id, workout_name="First Try")
    new_workout.save()
    assert new_workout.workout_name == "First Try"
    assert bool(new_workout.user_id) == True
    assert new_workout.complete == False
    assert len(new_workout.set_dicts_list) == 0
    assert len(new_workout.notes) == 0

def test_toggling_workout_complete(burrito_workout):
    print(f'{burrito_workout.user_weight =}')
    burrito_workout.toggle_complete()
    assert burrito_workout.complete == True

def test_toggling_workout_complete_twice(burrito_workout):
    burrito_workout.toggle_complete()
    assert burrito_workout.complete == True
    burrito_workout.toggle_complete()
    assert burrito_workout.complete == False

def test_adding_sets_dicts(burrito_workout):
    set_dict = SetDicts(exercise_name="Bench Press")
    burrito_workout.add_set_dict(set_dict)
    assert burrito_workout.set_dicts_list == [set_dict]


def test_add_workout_notes(burrito_workout):
    note = "Feel pretty good..."
    burrito_workout.add_notes(note)
    assert burrito_workout.notes == ["Feeling good", "Feel pretty good..."]

#TODO Create fixtures for future tests

def test_adding_sets_dict_object(burrito_workout, spoof_arnold_press_dict):
    burrito_workout.add_set_dict(spoof_arnold_press_dict)
    assert burrito_workout.set_dicts_list == [spoof_arnold_press_dict]

def test_adding_sets_dict_object_twice(burrito_workout, spoof_arnold_press_dict):
    set_dict = SetDicts(set_order=1, exercise_name="Arnold Press", set_number=1, set_type="Warm up", reps=12, loading=13.5, focus="Form", rest=60, notes="Shoulder warm up")
    burrito_workout.add_set_dict(spoof_arnold_press_dict)
    burrito_workout.add_set_dict(set_dict)
    assert burrito_workout.set_dicts_list == [spoof_arnold_press_dict, set_dict]

def test_to_dict_method(burrito_workout, spoofed_user_stats, spoof_arnold_press_dict):
    burrito_workout.add_stats(spoofed_user_stats)
    burrito_workout.add_set_dict(spoof_arnold_press_dict)

    expected_output = {
        "id": str(burrito_workout.id),
        "user_id": str(burrito_workout.user_id.id),
        "workout_name": burrito_workout.workout_name,
        "date": burrito_workout.date.isoformat() if burrito_workout.date else None,
        "complete": burrito_workout.complete,
        "sets_dict_list": [spoof_arnold_press_dict.to_dict()],
        "user_stats": burrito_workout.user_stats.to_dict() if burrito_workout.user_stats else None,
        "notes": burrito_workout.notes,
    }

    assert burrito_workout.to_dict() == expected_output

    
def test_delete_set_dict(burrito_workout, spoof_arnold_press_dict):
    burrito_workout.add_set_dict(spoof_arnold_press_dict)
    burrito_workout.add_set_dict(spoof_arnold_press_dict)
    assert burrito_workout.set_dicts_list == [spoof_arnold_press_dict, spoof_arnold_press_dict]
    burrito_workout.delete_set_dict(spoof_arnold_press_dict)
    assert burrito_workout.set_dicts_list == [spoof_arnold_press_dict]

def test_delete_workout_notes(burrito_workout):
    note_1 = "Feel pretty good..."
    note_2 = "Feel pretty mid..."
    note_3 = "Feel pretty bad..."
    burrito_workout.add_notes(note_1)
    burrito_workout.add_notes(note_2)
    burrito_workout.add_notes(note_3)
    burrito_workout.delete_note(0)
    burrito_workout.delete_note(-1)
    assert burrito_workout.notes == ["Feel pretty mid..."]