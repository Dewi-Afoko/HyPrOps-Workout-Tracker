# from lib.workout import Workout
# from unittest.mock import Mock
# from datetime import datetime

# def test_workout_creation_empty_values():
#     user1 = Mock()
#     workout1 = Workout(user1)
#     assert workout1.exercise_list == []

# def test_user_id_added_upon_creation():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     assert len(str(workout1.user_id)) > 0

# def test_date_injection():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     assert workout1.date == datetime.now().strftime("%Y/%m/%d")

# def test_incomplete_upon_creation():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     assert workout1.complete == False

# def test_adding_exercises():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     exercise = Mock()
#     workout1.add_exercise(exercise)
#     assert workout1.exercise_list == [exercise]

# def test_marking_complete():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     workout1.mark_complete()
#     assert workout1.complete == True

# def test__repr__():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     date = datetime.now().strftime("%Y/%m/%d")
#     assert workout1.__repr__() == f"Workout([], {workout1.user_id}, {date}, False)"

# def test___eq__true():
#     user1 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     workout2 = Workout(user1)
#     assert workout1.__eq__(workout2) == True

# def test___eq__false():
#     user1 = Mock(user_id = 1234)
#     user2 = Mock(user_id = 1234)
#     workout1 = Workout(user1)
#     workout2 = Workout(user2)
#     assert workout1.__eq__(workout2) == False