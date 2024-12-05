import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from models.set_dicts import SetDicts
from models.user_stats import UserStats
from models.personal_data import PersonalData
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from datetime import datetime

def test_personal_data_creation():
    new_data = PersonalData(name="Burrito", dob=11-12-2023, height=25, weight=25)
    assert new_data.name == "Burrito"
    assert new_data.dob == 11-12-2023
    assert new_data.weight == 25
    assert new_data.height == 25

def test_update_personal_data(spoofed_personal_data):
    assert spoofed_personal_data.name == "Burrito"
    assert spoofed_personal_data.dob.strftime('%Y/%m/%d') == "2021/11/12"
    assert spoofed_personal_data.weight == 25
    assert spoofed_personal_data.height == 25
    spoofed_personal_data.update_personal_details("Zan Ji", datetime(2020, 10, 10), 23, 20)
    assert spoofed_personal_data.name == "Zan Ji"
    assert spoofed_personal_data.dob.strftime('%Y/%m/%d') == "2020/10/10"
    assert spoofed_personal_data.weight == 20
    assert spoofed_personal_data.height == 23

def test_to_dict(spoofed_personal_data):
    assert spoofed_personal_data.to_dict() == {
            'name': 'Burrito',
            'dob': "2021/11/12",
            'height': 25,
            'weight': 25,
        }