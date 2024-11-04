from datetime import datetime
from lib.exercise import Exercise
from lib.user import User
from lib.workout import Workout
from lib.workout_exercise_info import Workout_Exercise_Info

def test_new_user_new_workout_new_exercise():
    user1 = User("Test")
    exercise1 = Exercise("Pull Up")
    workout1 = Workout(user1)
    workout1.add_exercise(exercise1)
    user1.add_workout(workout1)
    date = datetime.now().strftime("%Y/%m/%d")
    assert user1.__repr__() == f"User(Test, [{workout1}])"
    assert workout1.date == date
    assert workout1.exercise_list == [exercise1]

def test_new_user_new_workout_new_exercise_new_workout_info():
    user1 = User("Test")
    exercise1 = Exercise("Pull Up")
    workout1 = Workout(user1)
    details = Workout_Exercise_Info(workout1, exercise1)
    workout1.add_exercise(details)
    user1.add_workout(workout1)
    date = datetime.now().strftime("%Y/%m/%d")
    assert user1.__repr__() == f"User(Test, [{workout1}])"
    assert workout1.date == date
    assert workout1.exercise_list == [details]
