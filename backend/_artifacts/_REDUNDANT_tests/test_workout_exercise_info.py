# from lib.workout_exercise_info import Workout_Exercise_Info
# from unittest.mock import Mock

# def test_workout_id_passed_through():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     assert details.workout_id == 1

# def test_exercise_dict_created():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     assert details.exercise_dict == {"Test" : 
#                                 {"Reps" : [],
#                                 "Loading" : [],
#                                 "Rest" : [],
#                                 "Performance Notes" : []}
#                                 }

# def test_adding_sets():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.add_set(exercise1, 12)
#     assert details.exercise_dict["Test"]["Reps"] == [12]

# def test_adding_sets_thrice():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.add_set(exercise1, 12)
#     details.add_set(exercise1, 11)
#     details.add_set(exercise1, 8)
#     assert details.exercise_dict["Test"]["Reps"] == [12, 11, 8]

# def test_adding_loading():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.set_loading(exercise1, 120)
#     assert details.exercise_dict["Test"]["Loading"] == [120]

# def test_adding_rest():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.set_rest_period(exercise1, 120)
#     assert details.exercise_dict["Test"]["Rest"] == [120]

# def test_adding_notes():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.add_performance_notes(exercise1, "Merked it")
#     assert details.exercise_dict["Test"]["Performance Notes"] == ["Merked it"]

# def test_adding_loading_thrice():
#     workout1 = Mock()
#     exercise1 = Mock()
#     workout1.id = 1
#     exercise1.id = 1
#     exercise1.name = "Test"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.set_loading(exercise1, 120)
#     details.set_loading(exercise1, 110)
#     details.set_loading(exercise1, 80)
#     assert details.exercise_dict["Test"]["Loading"] == [120, 110, 80]

# def test_adding_exercise_adds_to_dict():
#     workout1 = Mock()
#     exercise1 = Mock()
#     exercise2 = Mock()
#     workout1.id = 1
#     exercise1.name = "Test"
#     exercise2.name = "Test2"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.add_exercise(exercise2)
#     assert details.exercise_dict == {"Test" : 
#                                 {"Reps" : [],
#                                 "Loading" : [],
#                                 "Rest" : [],
#                                 "Performance Notes" : []},
#                                 "Test2" : 
#                                 {"Reps" : [],
#                                 "Loading" : [],
#                                 "Rest" : [],
#                                 "Performance Notes" : []}
#                                 }

# def test_adding_exercise_adds_to_dict_and_add_reps_to_diff_exercises():
#     workout1 = Mock()
#     exercise1 = Mock()
#     exercise2 = Mock()
#     workout1.id = 1
#     exercise1.name = "Test"
#     exercise2.name = "Test2"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.add_exercise(exercise2)
#     details.add_set(exercise1, 12)
#     details.add_set(exercise1, 12)
#     details.add_set(exercise1, 12)
#     details.add_set(exercise2, 18)
#     details.add_set(exercise2, 18)
#     details.add_set(exercise2, 18)
#     assert details.exercise_dict == {"Test" : 
#                                 {"Reps" : [12, 12, 12],
#                                 "Loading" : [],
#                                 "Rest" : [],
#                                 "Performance Notes" : []},
#                                 "Test2" : 
#                                 {"Reps" : [18, 18, 18],
#                                 "Loading" : [],
#                                 "Rest" : [],
#                                 "Performance Notes" : []}
#                                 }
    
# def test___repr__():
#     workout1 = Mock()
#     exercise1 = Mock()
#     exercise2 = Mock()
#     workout1.id = 1
#     exercise1.name = "Test"
#     exercise2.name = "Test2"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details.add_exercise(exercise2)
#     expected_dict = repr({
#     "Test": {"Reps": [], "Loading": [], "Rest": [], "Performance Notes": []},
#     "Test2": {"Reps": [], "Loading": [], "Rest": [], "Performance Notes": []}})

#     assert details.__repr__() == f'Workout Exercise Info({details.workout_id}, {expected_dict})'

# def test___eq__():
#     workout1 = Mock()
#     exercise1 = Mock()
#     exercise2 = Mock()
#     workout1.id = 1
#     exercise1.name = "Test"
#     exercise2.name = "Test2"
#     details = Workout_Exercise_Info(workout1, exercise1)
#     details2 = Workout_Exercise_Info(workout1, exercise1)
#     details.add_exercise(exercise2)
#     details2.add_exercise(exercise2)
#     details.add_set(exercise1, 12)
#     details2.add_set(exercise1, 12)
#     details.add_set(exercise1, 12)
#     details2.add_set(exercise1, 12)
#     details2.add_set(exercise2, 18)
#     details.add_set(exercise2, 18)
#     details2.add_set(exercise2, 18)
#     details.add_set(exercise2, 18)
#     assert details.__eq__(details2)