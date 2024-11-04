from lib.workout_exercise_info import Workout_Exercise_Info
from unittest.mock import Mock

def test_workout_id_passed_through():
    workout1 = Mock()
    exercise1 = Mock()
    workout1.id = 1
    exercise1.name = "Test"
    details = Workout_Exercise_Info(workout1, exercise1)
    assert details.workout_id == 1

def test_exercise_dict_created():
    workout1 = Mock()
    exercise1 = Mock()
    workout1.id = 1
    exercise1.name = "Test"
    details = Workout_Exercise_Info(workout1, exercise1)
    assert details.exercise_dict == {"Test" : 
                                {"Reps" : [],
                                "Loading" : [],
                                "Rest" : [],
                                "Performance Notes" : []}
                                }

def test_adding_sets():
    workout1 = Mock()
    exercise1 = Mock()
    workout1.id = 1
    exercise1.id = 1
    exercise1.name = "Test"
    details = Workout_Exercise_Info(workout1, exercise1)
    details.add_set(exercise1, 12)
    assert details.exercise_dict["Test"]["Reps"] == [12]

def test_adding_sets_thrice():
    workout1 = Mock()
    exercise1 = Mock()
    workout1.id = 1
    exercise1.id = 1
    exercise1.name = "Test"
    details = Workout_Exercise_Info(workout1, exercise1)
    details.add_set(exercise1, 12)
    details.add_set(exercise1, 11)
    details.add_set(exercise1, 8)
    assert details.exercise_dict["Test"]["Reps"] == [12, 11, 8]

def test_adding_loading():
    workout1 = Mock()
    exercise1 = Mock()
    workout1.id = 1
    exercise1.id = 1
    exercise1.name = "Test"
    details = Workout_Exercise_Info(workout1, exercise1)
    details.set_loading(exercise1, 120)
    assert details.exercise_dict["Test"]["Loading"] == [120]

def test_adding_loading_thrice():
    workout1 = Mock()
    exercise1 = Mock()
    workout1.id = 1
    exercise1.id = 1
    exercise1.name = "Test"
    details = Workout_Exercise_Info(workout1, exercise1)
    details.set_loading(exercise1, 120)
    details.set_loading(exercise1, 110)
    details.set_loading(exercise1, 80)
    assert details.exercise_dict["Test"]["Loading"] == [120, 110, 80]
