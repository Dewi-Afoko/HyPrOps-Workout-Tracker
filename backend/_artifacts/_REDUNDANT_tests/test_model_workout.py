import pytest
from models.user import User
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo


def sample_workout(sample_user):
    workout = Workout(user_id=sample_user.id)
    workout.save()
    yield workout
    workout.delete()

def test_create_workout(sample_workout, sample_user):
    assert sample_workout.user_id == sample_user
    assert sample_workout.exercise_list == []  # No exercises initially

def test_add_exercise_to_workout(sample_workout):
    exercise_info = WorkoutExerciseInfo(exercise_name="Push-ups", reps=[10, 12], loading=[0.0, 0.0], rest=[60, 60])
    sample_workout.add_exercise(exercise_info)
    sample_workout.save()

    updated_workout = Workout.objects(id=sample_workout.id).first()
    assert len(updated_workout.exercise_list) == 1
    assert updated_workout.exercise_list[0].exercise_name == "Push-ups"
    assert updated_workout.exercise_list[0].reps == [10, 12]

def test_mark_workout_complete(sample_workout):
    sample_workout.mark_complete()
    assert sample_workout.complete is True

def test_create_workout_without_user():
    from mongoengine.errors import ValidationError
    with pytest.raises(ValidationError):
        workout = Workout()
        workout.save()

def test_workout_exercise_list_default():
    workout = Workout(user_id="some_user_id")
    workout.save()
    assert workout.exercise_list == []

def test_workout_repr(sample_workout_with_exercise):
    # Expected __repr__ output
    expected_repr = f"Workout(user_id={sample_workout_with_exercise.user_id}, exercise_list={sample_workout_with_exercise.exercise_list})"
    assert repr(sample_workout_with_exercise) == expected_repr

def test_workout_equality(sample_user):
    # Create two identical workouts
    workout1 = Workout(user_id=sample_user.id)
    workout1.exercise_list.append(WorkoutExerciseInfo(exercise_name="Push-ups", reps=[10, 12]))
    workout1.save()

    workout2 = Workout(user_id=sample_user.id)
    workout2.exercise_list.append(WorkoutExerciseInfo(exercise_name="Push-ups", reps=[10, 12]))
    workout2.save()

    # Fetch workouts from the database to ensure they are separate instances
    workout1_db = Workout.objects(id=workout1.id).first()
    workout2_db = Workout.objects(id=workout2.id).first()

    assert workout1_db == workout2_db  # Should be equal based on __eq__
    assert workout1_db is not workout2_db  # They should not be the same instance

