from datetime import datetime
from lib.exercise import Exercise
from lib.user import User
from lib.workout import Workout

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