import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from models.set_dicts import SetDicts
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from datetime import datetime

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
    set_dict_saved = SetDicts(exercise_name="Bench Press", set_order=1, set_number=1)
    assert burrito_workout.set_dicts_list[0] == set_dict_saved


def test_add_workout_notes(burrito_workout):
    note = "Feel pretty good..."
    burrito_workout.add_notes(note)
    assert burrito_workout.notes == ["Feeling good", "Feel pretty good..."]


def test_adding_sets_dict_object(burrito_workout, warm_up_shoulder_press):
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    assert burrito_workout.set_dicts_list == [warm_up_shoulder_press]

def test_adding_sets_dict_object_twice(burrito_workout, warm_up_shoulder_press):
    set_dict = SetDicts(set_order=1, exercise_name="Arnold Press", set_number=1, set_type="Warm up", reps=12, loading=13.5, focus="Form", rest=60, notes="Shoulder warm up")
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    burrito_workout.add_set_dict(set_dict)
    warm_up_saved =  SetDicts(set_order=1, exercise_name="Shoulder Press", set_number=1, set_type="Warm up", reps=12, loading=27.5, rest=45)
    set_dict_saved = SetDicts(set_order=2, exercise_name="Arnold Press", set_number=1, set_type="Warm up", reps=12, loading=13.5, focus="Form", rest=60, notes="Shoulder warm up")
    assert burrito_workout.set_dicts_list == [warm_up_saved, set_dict_saved]

def test_to_dict_method(burrito_workout, warm_up_shoulder_press):
    burrito_workout.add_set_dict(warm_up_shoulder_press)


    expected_output = {
        "id": str(burrito_workout.id),
        "user_id": str(burrito_workout.user_id.id),
        "workout_name": burrito_workout.workout_name,
        "date": burrito_workout.date.strftime('%Y/%m/%d'),
        "complete": burrito_workout.complete,
        "set_dicts_list": [warm_up_shoulder_press.to_dict()],
        "notes": burrito_workout.notes,
        "sleep_score" : burrito_workout.sleep_score,
        "sleep_quality" : burrito_workout.sleep_quality,
        "user_weight" : burrito_workout.user_weight,
    }

    assert burrito_workout.to_dict() == expected_output

    
def test_delete_set_dict(burrito_workout, warm_up_shoulder_press):
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    burrito_workout.delete_set_dict(1)
    warm_up_saved =  SetDicts(set_order=1, exercise_name="Shoulder Press", set_number=1, set_type="Warm up", reps=12, loading=27.5, rest=45)
    assert burrito_workout.set_dicts_list == [warm_up_saved]

def test_delete_workout_notes(burrito_workout):
    note_1 = "Feel pretty good..."
    note_2 = "Feel pretty mid..."
    note_3 = "Feel pretty bad..."
    burrito_workout.add_notes(note_1)
    burrito_workout.add_notes(note_2)
    burrito_workout.add_notes(note_3)
    burrito_workout.delete_note(0)
    burrito_workout.delete_note(0)
    burrito_workout.delete_note(-1)
    assert burrito_workout.notes == ["Feel pretty mid..."]

def test_dynamic_set_order_and_set_number(burrito_workout, warm_up_shoulder_press):
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    burrito_workout.save()
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    burrito_workout.save()
    burrito_workout.add_set_dict(warm_up_shoulder_press)
    burrito_workout.save()
    assert burrito_workout.set_dicts_list[0].set_order == 1
    assert burrito_workout.set_dicts_list[1].set_order == 2
    assert burrito_workout.set_dicts_list[2].set_order == 3


def test_edit_workout_details(burrito_workout):
    burrito_workout.edit_details(name="Edited Name", date=datetime.strptime("2025/01/01", "%Y/%m/%d"), sleep_score=60, sleep_quality="Meh")
    assert burrito_workout.workout_name == "Edited Name"
    assert burrito_workout.date == datetime.strptime("2025/01/01", "%Y/%m/%d")
    assert burrito_workout.sleep_score == 60
    assert burrito_workout.sleep_quality == "Meh"
    assert burrito_workout.user_weight == 35