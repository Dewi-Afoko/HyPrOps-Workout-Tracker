# import pytest
# from models.user import User
# from models.workout import Workout
# from models.workout_exercise_info import WorkoutExerciseInfo


# def test_add_exercise_to_workout(sample_workout):
#     # Create a WorkoutExerciseInfo instance and add it to the workout
#     exercise_info = WorkoutExerciseInfo(
#         exercise_name="Push-ups", 
#         reps=[10, 12], 
#         loading=[0.0, 0.0], 
#         rest=[60, 60], 
#         performance_notes=["Felt strong", "Maintain form"]
#     )
#     sample_workout.add_exercise(exercise_info)
#     sample_workout.save()

#     # Fetch the workout again to verify the embedded document
#     updated_workout = Workout.objects(id=sample_workout.id).first()
#     assert len(updated_workout.exercise_list) == 1
#     assert updated_workout.exercise_list[0].exercise_name == "Push-ups"
#     assert updated_workout.exercise_list[0].reps == [10, 12]
#     assert updated_workout.exercise_list[0].loading == [0.0, 0.0]
#     assert updated_workout.exercise_list[0].rest == [60, 60]
#     assert updated_workout.exercise_list[0].performance_notes == ["Felt strong", "Maintain form"]

# def test_add_workout_to_user(sample_user):
#     # Create a Workout and link it to the user
#     workout = Workout(user_id=sample_user.id)
#     workout.save()
#     sample_user.add_workout(workout)
#     sample_user.save()

#     # Fetch the user again to verify the linked workout
#     updated_user = User.objects(id=sample_user.id).first()
#     assert len(updated_user.workout_list) == 1
#     assert updated_user.workout_list[0].id == workout.id

# def test_add_exercise_and_link_to_user(sample_user):
#     # Create a Workout and add a WorkoutExerciseInfo instance to it
#     workout = Workout(user_id=sample_user.id)
#     exercise_info = WorkoutExerciseInfo(exercise_name="Squats", reps=[5, 5], loading=[100, 105], rest=[90, 90])
#     workout.exercise_list.append(exercise_info)
#     workout.save()

#     # Link the workout to the user
#     sample_user.workout_list.append(workout)
#     sample_user.save()

#     # Fetch the user and workout to verify
#     updated_user = User.objects(id=sample_user.id).first()
#     updated_workout = Workout.objects(id=workout.id).first()

#     # Verify the user has the workout in their workout_list
#     assert len(updated_user.workout_list) == 1
#     assert updated_user.workout_list[0].id == workout.id

#     # Verify the workout has the correct exercise info
#     assert len(updated_workout.exercise_list) == 1
#     assert updated_workout.exercise_list[0].exercise_name == "Squats"
#     assert updated_workout.exercise_list[0].reps == [5, 5]
#     assert updated_workout.exercise_list[0].loading == [100, 105]
#     assert updated_workout.exercise_list[0].rest == [90, 90]
