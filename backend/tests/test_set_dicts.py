import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from models.set_dicts import SetDicts
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError

def test_creation_of_dict_variables():
    set_dict = SetDicts(set_order=1, exercise_name="Arnold Press", set_number=1, set_type="Warm up", reps=12, loading=13.5, focus="Form", rest=60, notes="Shoulder warm up")
    assert set_dict.set_order == 1
    assert set_dict.set_number == 1
    assert set_dict.exercise_name == "Arnold Press"
    assert set_dict.set_type == "Warm up"
    assert set_dict.reps == 12
    assert 14 > set_dict.loading > 13
    assert set_dict.focus == "Form"
    assert set_dict.rest == 60
    assert set_dict.notes == "Shoulder warm up"
    assert set_dict.complete == False

def test_toggle_complete(spoof_arnold_press_dict):
    spoof_arnold_press_dict.toggle_complete()
    assert spoof_arnold_press_dict.complete == True

def test_toggle_complete_twice(spoof_arnold_press_dict):
    assert spoof_arnold_press_dict.complete == False
    spoof_arnold_press_dict.toggle_complete()
    assert spoof_arnold_press_dict.complete == True
    spoof_arnold_press_dict.toggle_complete()
    assert spoof_arnold_press_dict.complete == False

def test_add_notes(spoof_arnold_press_dict):
    spoof_arnold_press_dict.add_notes("Let's go!")
    assert spoof_arnold_press_dict.notes == "Let's go!"

def test_delete_notes(spoof_arnold_press_dict):
    spoof_arnold_press_dict.add_notes("Let's go!")
    assert spoof_arnold_press_dict.notes == "Let's go!"
    spoof_arnold_press_dict.delete_notes()
    assert spoof_arnold_press_dict.notes == None