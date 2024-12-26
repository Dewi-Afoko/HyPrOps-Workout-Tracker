import pytest
import os
from dotenv import load_dotenv
from models.user import User
from models.workout import Workout
from models.set_dicts import SetDicts
from models.user_stats import UserStats
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError

def test_user_stats_creation(spoofed_personal_data):
    stats = UserStats(weight=25, sleep_score=80, sleep_quality="Great", notes="Ready to get it!")
    assert stats.weight == 25
    assert stats.sleep_score == 80
    assert stats.sleep_quality == "Great"
    assert stats.notes == "Ready to get it!"

def test_update_user_stats(spoofed_user_stats):
    assert spoofed_user_stats.weight == 25
    assert spoofed_user_stats.notes == "Ready to start!"
    assert spoofed_user_stats.sleep_quality == "Great"
    assert spoofed_user_stats.sleep_score == 80

    spoofed_user_stats.update_user_stats(notes="We good", weight=250, sleep_score=65, sleep_quality="Bad")
    assert spoofed_user_stats.weight == 250
    assert spoofed_user_stats.notes == "We good"
    assert spoofed_user_stats.sleep_quality == "Bad"
    assert spoofed_user_stats.sleep_score == 65