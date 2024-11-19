from flask import Blueprint, request, jsonify
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo
from bson import ObjectId

workout_details_bp = Blueprint('exercise', __name__)

@workout_details_bp.route('/workouts/<user_id>/<workout_id>/add_exercise', methods=['POST'])
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
def add_details_to_exercise_info(user_id, workout_id):
        workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
        if not workout:
            return jsonify({"error": "Workout not found"}), 404
        data = request.get_json()

    # Payload logic for empty fields
        response_payload = {}
        for entry in workout['exercise_list']:
            if data['exercise_name'] in entry['exercise_name']: # Exercise name required to identify where to add these values
                if "reps" in data and data["reps"] > 0:
                    response_payload['reps'] = data['reps']
                    entry.add_set(data['reps'])
                if 'loading' in data and data["loading"] > 0:
                    response_payload['loading'] = data['loading']
                    entry.set_loading(data['loading'])
                if 'rest' in data and data["rest"] > 0:
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
