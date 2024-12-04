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

def test_personal_data_creation():
    new_data = PersonalData(name="Burrito", dob=11-12-2023, height=25, weight=25)
    assert new_data.name == "Burrito"
    assert new_data.dob == 11-12-2023
    assert new_data.weight == 25
    assert new_data.height == 25