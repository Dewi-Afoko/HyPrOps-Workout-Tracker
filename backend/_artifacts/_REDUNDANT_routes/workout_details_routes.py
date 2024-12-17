from flask import Blueprint, request, jsonify
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo
from models.user import User
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity

workout_details_bp = Blueprint('workout_details_bp', __name__)

@workout_details_bp.route('/workouts/<user_id>/<workout_id>', methods=['GET'])
@jwt_required()
def get_specific_workout(user_id, workout_id):
    workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    

    return jsonify({"workout": workout.to_dict()}), 200


@workout_details_bp.route('/workouts/<user_id>/<workout_id>/add_exercise', methods=['POST'])
@jwt_required()
def create_workout_exercise_info(user_id, workout_id):
    workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()
    for entry in workout['exercise_list']:
        if data['exercise_name'] in entry['exercise_name']:
            return jsonify({"error": "Exercise already exists, try adding details!"}), 418

    details = WorkoutExerciseInfo(exercise_name=data['exercise_name'])
    workout.add_exercise(details)
    return jsonify({"workout id": str(workout.id), "exercise added": str(details.exercise_name)}), 201

@workout_details_bp.route('/workouts/<user_id>/<workout_id>/add_details', methods=['PATCH'])
@jwt_required()
def add_details_to_exercise_info(user_id, workout_id):
        workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
        if not workout:
            return jsonify({"error": "Workout not found"}), 404
        data = request.get_json()

    # Payload logic for empty fields
        response_payload = {}
        for entry in workout['exercise_list']:
            if data['exercise_name'] in entry['exercise_name']: # Exercise name required to identify where to add these values
                if "reps" in data and data["reps"] != None:
                    response_payload['reps'] = data['reps']
                    entry.add_set(data['reps'])
                if 'loading' in data and data["loading"] != None:
                    response_payload['loading'] = data['loading']
                    entry.set_loading(data['loading'])
                if 'rest' in data and data["rest"] != None:
                    response_payload['rest'] = data['rest']
                    entry.set_rest_period(data['rest'])
                if 'notes' in data and len(data["notes"]) > 0:
                    response_payload['notes'] = data['notes']
                    entry.add_performance_notes(data['notes'])
                workout.save()
                return jsonify(response_payload), 201
        else:
                return jsonify({"error" : "Exercise not found!"}), 418
        
@workout_details_bp.route('/workouts/<user_id>/<workout_id>/edit_details', methods=['PATCH'])
@jwt_required()
def edit_details_in_exercise_info(user_id, workout_id):
    workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()

    # Retrieve exercise name and locate the exercise in the workout
    exercise_name = data.get('exercise_name')
    if not exercise_name:
        return jsonify({"error": "Exercise name is required"}), 400

    exercise_info = next((exercise for exercise in workout.exercise_list if exercise.exercise_name == exercise_name), None)
    if not exercise_info:
        return jsonify({"error": "Exercise not found"}), 404

    # Build the payload for the edit_details method
    payload = {}
    if 'reps_index' in data and 'reps_value' in data:
        payload['reps_index'] = data['reps_index']
        payload['reps_value'] = data['reps_value']
    if 'performance_notes_index' in data and 'performance_notes_value' in data:
        payload['performance_notes_index'] = data['performance_notes_index']
        payload['performance_notes_value'] = data['performance_notes_value']

    # Apply updates via edit_details method
    response = exercise_info.edit_details(**payload)

    # Save the workout if any updates were made
    if 'message' not in response or response['message'] != 'No details to update provided or indices out of range':
        workout.save()

    # Return the response
    if 'error' in response:
        return jsonify(response), 400
    elif 'message' in response and response['message'] == 'No details to update provided or indices out of range':
        return jsonify(response), 400
    else:
        return jsonify(response), 200

@workout_details_bp.route('/workouts/<user_id>/<workout_id>/<exercise_name>', methods=['PATCH'])
@jwt_required()
def complete_set(user_id, workout_id, exercise_name):
    # Find the user
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Find the workout
    workout = Workout.objects(id=workout_id).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    # Find the exercise in the workout's exercise_list
    exercise = next((ex for ex in workout.exercise_list if ex.exercise_name == exercise_name), None)
    if not exercise:
        return jsonify({"error": f"Exercise '{exercise_name}' not found in workout"}), 404

    # Call the mark_complete method on the exercise
    exercise.mark_complete()

    # Save the workout document to persist changes to the exercise
    workout.save()

    return jsonify({"message": "Exercise status updated", "exercise": str(exercise.complete)}), 200

@workout_details_bp.route('/workouts/<user_id>/<workout_id>/delete_details', methods=['DELETE'])
@jwt_required()
def delete_details_in_exercise_info(user_id, workout_id):
    workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()
    exercise_name = data.get('exercise_name')

    if not exercise_name:
        return jsonify({"error": "Exercise name is required"}), 400

    exercise_info = next((exercise for exercise in workout.exercise_list if exercise.exercise_name == exercise_name), None)

    if not exercise_info:
        return jsonify({"error": "Exercise not found"}), 404

    # Debug: Ensure exercise_info is of the correct type
    print(f"Type of exercise_info: {type(exercise_info)}")

    # Ensure exercise_info is of type WorkoutExerciseInfo
    if not isinstance(exercise_info, WorkoutExerciseInfo):
        return jsonify({"error": "Invalid exercise information type"}), 400

    payload = {}
    for key in ['reps_index', 'loading_index', 'rest_index', 'performance_notes_index']:
        if key in data:
            if isinstance(data[key], list):
                payload[key] = data[key]
            else:
                return jsonify({"error": f"{key} must be a list of indices"}), 400

    response = exercise_info.delete_details(**payload)

    if 'message' not in response or response['message'] != 'No valid details to delete or indices out of range':
        workout.save()

    if 'error' in response:
        return jsonify(response), 400
    elif 'message' in response and response['message'] == 'No valid details to delete or indices out of range':
        return jsonify(response), 400
    else:
        return jsonify(response), 200


@workout_details_bp.route('/workouts/<user_id>/<workout_id>/delete_exercise', methods=['DELETE'])
@jwt_required()
def delete_exercise(user_id, workout_id):
    workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()
    if not data['exercise_name']:
            return jsonify({"error": "Exercise not found,in request data"}), 418

    details = WorkoutExerciseInfo(exercise_name=data['exercise_name'])
    workout.delete_exercise(details)
    return jsonify({"workout id": str(workout.id), "exercise deleted": str(details.exercise_name)}), 200