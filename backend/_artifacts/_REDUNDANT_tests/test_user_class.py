from lib.user import User
from unittest.mock import Mock

def test_creating_user_sets_username():
    user1 = User("FirstUp")
    assert user1.username == "FirstUp"

def test_creating_user_sets_empty_exercise_list():
    user1 = User("FirstUp")
    assert user1.workout_list == []

def test_adding_password():
    user1 = User("FirstUp")
    user1.update_password("password")
    assert user1.password == "password"

def test_adding_mock_workout():
    user1 = User("FirstUp")
    mockcercise = Mock()
    user1.add_workout(mockcercise)
    assert user1.workout_list == [mockcercise]

def test_eq_method_true():
    user1 = User("FirstUp")
    user2 = User("FirstUp")
    assert user1 == user2


def test_eq_method_untrue():
    user1 = User("FirstUp")
    user2 = User("FirstUppppp")
    assert user1 != user2

def test_repr_method():
    user1 = User("FirstUp")
    assert user1.__repr__() == "User(FirstUp, [])"