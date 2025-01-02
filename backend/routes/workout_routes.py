from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import User, Workout, SetDicts
from lib.utilities.api_functions import find_set_dicts, find_single_set_dict, find_single_workout, find_user_from_jwt, find_user_workouts_list, workouts_as_dict, check_for_error
from mongoengine import ValidationError

workouts_bp = Blueprint('workouts', __name__)

# FUNCTIONALITY Get User Workouts

@workouts_bp.route('/workouts', methods=['GET'])
@jwt_required()
def get_all_workouts():
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workouts = find_user_workouts_list()
    workouts_dicts = workouts_as_dict(workouts)

    if check_for_error(workouts_dicts):
        return workouts_dicts

    return jsonify({
    'message': 'Here are your workouts:',
    'workouts': workouts_dicts
}), 200

# FUNCTIONALITY Get single workout by ID

@workouts_bp.route('/workouts/<workout_id>', methods=['GET'])
@jwt_required()
def get_single_workout(workout_id):
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    
    return jsonify({
    'message': f'Here are the details for workout ID: {workout_id}',
    'workout': workout.to_dict()
}), 200

# FUNCTIONALITY Create workout

@workouts_bp.route('/workouts', methods=['POST'])
@jwt_required()
def create_workout():
    data = request.get_json()
    if 'workout_name' not in data.keys():
        return jsonify({'error' : 'You need to name your workout'}), 400
    user = find_user_from_jwt()
    if check_for_error(user):
        return user

    workout = Workout(user_id=str(user.id), workout_name=data['workout_name'])
    workout.save()


    return jsonify({'message' : f'{workout.workout_name} created by {user.username}'}), 201

# FUNCTIONALITY Add notes to a workout

@workouts_bp.route('/workouts/<workout_id>/add_notes', methods=['PATCH'])
@jwt_required()
def add_workout_notes(workout_id):
    data = request.get_json()
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    workout.add_notes(data.get('notes'))

    return jsonify({'message' : f'{data.get("notes")}: added to workout notes'}), 200

# FUNCTIONALITY Delete notes from workout by index positon

@workouts_bp.route('/workouts/<workout_id>/delete_note/<note_index>', methods=['DELETE'])
@jwt_required()
def delete_workout_note(workout_id, note_index):
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    
    workout.delete_note(note_index)


    return jsonify({'message' : 'Note successfully deleted'}), 200

# FUNCTIONALITY Toggle workout completion status

@workouts_bp.route('/workouts/<workout_id>/mark_complete', methods=['PATCH'])
@jwt_required()
def toggle_workout_complete(workout_id):
    
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    
    workout.toggle_complete()
    
    if workout.complete == True:
        status = "complete"
    elif workout.complete == False:
        status = "incomplete"

    return jsonify({'message' : f'Workout marked as {status}'}), 200


# FUNCTIONALITY Create SetDict and add to workout


@workouts_bp.route('/workouts/<workout_id>/add_set', methods=['POST'])
@jwt_required()
def add_set_dict(workout_id):

    data = request.get_json()

    if 'exercise_name' not in data.keys():
        return jsonify({'error' : 'You need to specify an exercise'}), 400
    
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    
    set_order = (len(workout.set_dicts_list) + 1)
    
    set_number = len([set for set in workout.set_dicts_list if set.exercise_name == data['exercise_name']])

    try:
        set_dict = SetDicts(set_order=set_order, exercise_name=data.get('exercise_name'), set_number=set_number, set_type=data.get('set_type'), reps=data.get('reps'), loading=data.get('loading'), focus=data.get('focus'), rest=data.get('rest'), notes=data.get('notes'))

        workout.add_set_dict(set_dict)
        user.save()

        return jsonify({'message': f'Set info for {set_dict.exercise_name} created and added to {workout.workout_name}'}), 201

    except(ValidationError):
        return jsonify({'error' : 'Failure to create set dictionary'}), 400     
    

# FUNCTIONALITY Mark SetDict as complete
    

@workouts_bp.route('/workouts/<workout_id>/<set_order>/mark_complete', methods=['PATCH'])
@jwt_required()
def toggle_set_complete(workout_id, set_order):

    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout
    

    set_dict = next((set for set in workout.set_dicts_list if set.set_order == int(set_order)), None)

    set_dict.toggle_complete()
    workout.save()
    user.save()
    if set_dict.complete == True:
        return jsonify({'message' : 'Set marked complete'}), 200
    elif set_dict.complete == False:
        return jsonify({'message' : 'Set marked incomplete'}), 200
    

# FUNCTIONALITY Add/replace notes for SetDict
    
@workouts_bp.route('/workouts/<workout_id>/<set_order>/add_notes', methods=['PATCH'])
@jwt_required()
def add_notes_to_set(workout_id, set_order):
    data = request.get_json()
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout

    set_dict = next((set for set in workout.set_dicts_list if set.set_order == int(set_order)), None)

    set_dict.add_notes(data.get('notes'))
    workout.save()
    user.save()

    return jsonify({'message' : 'Notes added to set'}), 201

# FUNCTIONALITY Delete notes from SetDict

@workouts_bp.route('/workouts/<workout_id>/<set_order>/delete_notes', methods=['DELETE'])
@jwt_required()
def delete_set_notes(workout_id, set_order):
    user = find_user_from_jwt()
    if check_for_error(user):
        return user
    
    workout = find_single_workout(workout_id)
    if check_for_error(workout):
        return workout

    set_dict = next((set for set in workout.set_dicts_list if set.set_order == int(set_order)), None)

    set_dict.delete_notes()
    workout.save()
    user.save()

    return jsonify({'message' : 'Notes deleted'}), 200
