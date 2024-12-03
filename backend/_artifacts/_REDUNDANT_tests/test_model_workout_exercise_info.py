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
    expected_repr = "WorkoutExerciseInfo(exercise_name=Pull-ups, reps=[10, 12], loading=[], rest=[], performance_notes=[], complete=False)"
    assert repr(exercise_info) == expected_repr

import pytest
from models.workout_exercise_info import WorkoutExerciseInfo

# Test updating a specific entry in reps
def test_edit_reps():
    exercise_info = WorkoutExerciseInfo(reps=[10, 12])
    response = exercise_info.edit_details(reps_index=1, reps_value=15)
    assert exercise_info.reps[1] == 15
    assert response == {'updated_reps': 'reps[1] = 15'}

# Test updating a specific entry in loading
def test_edit_loading():
    exercise_info = WorkoutExerciseInfo(loading=[50.0, 55.0])
    response = exercise_info.edit_details(loading_index=0, loading_value=52.5)
    assert exercise_info.loading[0] == 52.5
    assert response == {'updated_loading': 'loading[0] = 52.5'}

# Test updating a specific entry in rest
def test_edit_rest():
    exercise_info = WorkoutExerciseInfo(rest=[60, 60])
    response = exercise_info.edit_details(rest_index=1, rest_value=75)
    assert exercise_info.rest[1] == 75
    assert response == {'updated_rest': 'rest[1] = 75'}

# Test updating a specific entry in performance_notes
def test_edit_performance_notes():
    exercise_info = WorkoutExerciseInfo(performance_notes=["Good form", "Increase weight"])
    response = exercise_info.edit_details(performance_notes_index=0, performance_notes_value="Focus on breathing")
    assert exercise_info.performance_notes[0] == "Focus on breathing"
    assert response == {'updated_performance_notes': 'performance_notes[0] = Focus on breathing'}

# Test handling an out-of-range index for reps
def test_out_of_range_reps():
    exercise_info = WorkoutExerciseInfo(reps=[10, 12])
    response = exercise_info.edit_details(reps_index=5, reps_value=20)
    assert response == {'reps_error': 'Index 5 out of range for reps'}
    assert exercise_info.reps == [10, 12]  # Ensure reps list was not modified

# Test handling an out-of-range index for loading
def test_out_of_range_loading():
    exercise_info = WorkoutExerciseInfo(loading=[50.0, 55.0])
    response = exercise_info.edit_details(loading_index=3, loading_value=60.0)
    assert response == {'loading_error': 'Index 3 out of range for loading'}
    assert exercise_info.loading == [50.0, 55.0]  # Ensure loading list was not modified

# Test handling an out-of-range index for rest
def test_out_of_range_rest():
    exercise_info = WorkoutExerciseInfo(rest=[60, 60])
    response = exercise_info.edit_details(rest_index=2, rest_value=90)
    assert response == {'rest_error': 'Index 2 out of range for rest'}
    assert exercise_info.rest == [60, 60]  # Ensure rest list was not modified

# Test handling an out-of-range index for performance_notes
def test_out_of_range_performance_notes():
    exercise_info = WorkoutExerciseInfo(performance_notes=["Good form", "Increase weight"])
    response = exercise_info.edit_details(performance_notes_index=2, performance_notes_value="Focus more")
    assert response == {'performance_notes_error': 'Index 2 out of range for performance notes'}
    assert exercise_info.performance_notes == ["Good form", "Increase weight"]  # Ensure performance_notes list was not modified

# Test handling of no updates
def test_no_updates_provided():
    exercise_info = WorkoutExerciseInfo(reps=[10, 12], loading=[50.0, 55.0], rest=[60, 60], performance_notes=["Good form", "Increase weight"])
    response = exercise_info.edit_details()
    assert response == {'message': 'No details to update provided or indices out of range'}

# Test updating multiple entries at once
def test_edit_multiple_fields():
    exercise_info = WorkoutExerciseInfo(reps=[10, 12], loading=[50.0, 55.0])
    response = exercise_info.edit_details(
        reps_index=0, reps_value=8,
        loading_index=1, loading_value=60.0
    )
    assert exercise_info.reps[0] == 8
    assert exercise_info.loading[1] == 60.0
    assert response == {
        'updated_reps': 'reps[0] = 8',
        'updated_loading': 'loading[1] = 60.0'
    }