import pytest
from models.workout_exercise_info import WorkoutExerciseInfo
from models.workout import Workout
from mongoengine.errors import ValidationError

def test_create_workout_exercise_info():
    exercise_info = WorkoutExerciseInfo(exercise_name="Push-ups")
    
    assert exercise_info.exercise_name == "Push-ups"
    assert exercise_info.reps == []
    assert exercise_info.loading == []
    assert exercise_info.rest == []
    assert exercise_info.performance_notes == []

def test_add_set():
    exercise_info = WorkoutExerciseInfo(exercise_name="Push-ups")
    exercise_info.add_set(10)
    exercise_info.add_set(12)
    
    assert exercise_info.reps == [10, 12]

def test_set_loading():
    exercise_info = WorkoutExerciseInfo(exercise_name="Bench Press")
    exercise_info.set_loading(100.5)
    exercise_info.set_loading(105.0)
    
    assert exercise_info.loading == [100.5, 105.0]

def test_set_rest_period():
    exercise_info = WorkoutExerciseInfo(exercise_name="Squats")
    exercise_info.set_rest_period(60)
    exercise_info.set_rest_period(90)
    
    assert exercise_info.rest == [60, 90]

def test_add_performance_notes():
    exercise_info = WorkoutExerciseInfo(exercise_name="Deadlift")
    exercise_info.add_performance_notes("Good form")
    exercise_info.add_performance_notes("Need to improve depth")
    
    assert exercise_info.performance_notes == ["Good form", "Need to improve depth"]

def test_equality():
    exercise_info1 = WorkoutExerciseInfo(exercise_name="Pull-ups")
    exercise_info1.add_set(8)
    exercise_info1.set_loading(0)  # Bodyweight
    exercise_info1.set_rest_period(60)
    exercise_info1.add_performance_notes("Strong start")

    exercise_info2 = WorkoutExerciseInfo(exercise_name="Pull-ups")
    exercise_info2.add_set(8)
    exercise_info2.set_loading(0)  # Bodyweight
    exercise_info2.set_rest_period(60)
    exercise_info2.add_performance_notes("Strong start")

    assert exercise_info1 == exercise_info2  # Uses __eq__ method to compare

def test_create_workout_exercise_info_without_name(sample_user):
    # Create Workout and add WorkoutExerciseInfo without an exercise_name
    workout = Workout(user_id=sample_user.id)
    workout.exercise_list.append(WorkoutExerciseInfo())  # Missing exercise_name
    with pytest.raises(ValidationError):
        workout.save()  # Attempt to save workout with invalid embedded document

def test_workout_exercise_info_defaults():
    exercise_info = WorkoutExerciseInfo(exercise_name="Push-ups")
    assert exercise_info.reps == []
    assert exercise_info.loading == []
    assert exercise_info.rest == []
    assert exercise_info.performance_notes == []

def test_workout_exercise_info_repr():
    exercise_info = WorkoutExerciseInfo(exercise_name="Pull-ups", reps=[10, 12])
    expected_repr = "WorkoutExerciseInfo(exercise_name=Pull-ups, reps=[10, 12], loading=[], rest=[], performance_notes=[])"
    assert repr(exercise_info) == expected_repr

