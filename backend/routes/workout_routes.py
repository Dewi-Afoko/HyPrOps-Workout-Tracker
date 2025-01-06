from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import User, Workout, SetDicts
from lib.utilities.helper_functions import find_set_dicts, find_single_set_dict, find_single_workout, find_user_from_jwt, find_user_workouts_list, workouts_as_dict, check_for_error
from mongoengine import ValidationError
from flask_restx import Resource
from .restx_models import workout_ns, workout_get_success, workout_get_failure, single_workout_success, single_workout_failure, create_workout_request, create_workout_success, create_workout_failure, notes_request, notes_success, notes_failure, mark_complete_success, add_set_request, add_set_success, add_set_failure, mark_set_complete_success



@workout_ns.route('')
class Workouts(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', workout_get_success),
        404: ('Not Found', workout_get_failure),
    })
    def get(self):
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workouts = find_user_workouts_list()
        workouts_dicts = workouts_as_dict(workouts)
        if check_for_error(workouts_dicts):
            return workouts_dicts
        
        return {'message': 'Here are your workouts:', 'workouts': workouts_dicts}, 200

    @jwt_required()
    @workout_ns.expect(create_workout_request)
    @workout_ns.doc(responses={
        201: ('Created', create_workout_success),
        400: ('Bad Request', create_workout_failure),
    })
    def post(self):
        """Create a new workout"""
        data = request.get_json()
        if 'workout_name' not in data:
            return {'error': 'You need to name your workout'}, 400
        
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = Workout(user_id=str(user.id), workout_name=data['workout_name'])
        workout.save()
        return {'message': f'{workout.workout_name} created by {user.username}', 'workout': workout.to_dict()}, 201


@workout_ns.route('/<string:workout_id>')
class SingleWorkout(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', single_workout_success),
        404: ('Not Found', single_workout_failure),
    })
    def get(self, workout_id):
        """Get a single workout by ID"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        return {'message': f'Here are the details for workout ID: {workout_id}', 'workout': workout.to_dict()}, 200


@workout_ns.route('/<string:workout_id>/add_notes')
class AddWorkoutNotes(Resource):
    @jwt_required()
    @workout_ns.expect(notes_request)
    @workout_ns.doc(responses={
        200: ('Success', notes_success),
        400: ('Bad Request', notes_failure),
    })
    def patch(self, workout_id):
        """Add notes to a workout"""
        data = request.get_json()
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        workout.add_notes(data.get('notes'))
        return {'message': f'{data.get("notes")}: added to workout notes'}, 200


@workout_ns.route('/<string:workout_id>/delete_note/<int:note_index>')
class DeleteWorkoutNote(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', notes_success),
        404: ('Not Found', notes_failure),
    })
    def delete(self, workout_id, note_index):
        """Delete a note from a workout by index"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        workout.delete_note(note_index)
        return {'message': 'Note successfully deleted'}, 200


@workout_ns.route('/<string:workout_id>/mark_complete')
class ToggleWorkoutComplete(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', mark_complete_success),
    })
    def patch(self, workout_id):
        """Toggle the completion status of a workout"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        workout.toggle_complete()
        status = "complete" if workout.complete else "incomplete"
        return {'message': f'Workout marked as {status}'}, 200


@workout_ns.route('/<string:workout_id>/add_set')
class AddSetToWorkout(Resource):
    @jwt_required()
    @workout_ns.expect(add_set_request)
    @workout_ns.doc(responses={
        201: ('Created', add_set_success),
        400: ('Bad Request', add_set_failure),
    })
    def post(self, workout_id):
        """Add a set to a workout"""
        data = request.get_json()
        if 'exercise_name' not in data:
            return {'error': 'You need to specify an exercise'}, 400
        
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        set_order = len(workout.set_dicts_list) + 1
        set_number = len([set for set in workout.set_dicts_list if set.exercise_name == data['exercise_name']])

        try:
            set_dict = SetDicts(
                set_order=set_order, exercise_name=data.get('exercise_name'),
                set_number=set_number, set_type=data.get('set_type'),
                reps=data.get('reps'), loading=data.get('loading'),
                focus=data.get('focus'), rest=data.get('rest'),
                notes=data.get('notes')
            )

            workout.add_set_dict(set_dict)
            user.save()
            return {'message': f'Set info for {set_dict.exercise_name} created and added to {workout.workout_name}'}, 201
        except ValidationError:
            return {'error': 'Failure to create set dictionary'}, 400
        
@workout_ns.route('/<string:workout_id>/<int:set_order>/mark_complete')
class MarkSetComplete(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', mark_set_complete_success),
    })
    def patch(self, workout_id, set_order):
        """Mark a set as complete or incomplete"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        set_dict = next((set for set in workout.set_dicts_list if set.set_order == set_order), None)
        if not set_dict:
            return {'error': 'Set not found'}, 404
        
        set_dict.toggle_complete()
        workout.save()
        return {'message': 'Set marked complete' if set_dict.complete else 'Set marked incomplete'}, 200

@workout_ns.route('/<string:workout_id>/<int:set_order>/add_notes')
class AddNotesToSet(Resource):
    @jwt_required()
    @workout_ns.expect(notes_request)
    @workout_ns.doc(responses={
        201: ('Created', notes_success),
        400: ('Bad Request', notes_failure),
    })
    def patch(self, workout_id, set_order):
        """Add or replace notes for a set in a workout"""
        data = request.get_json()
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        set_dict = next((set for set in workout.set_dicts_list if set.set_order == set_order), None)
        if not set_dict:
            return {'error': 'Set not found'}, 404
        
        set_dict.add_notes(data.get('notes'))
        workout.save()
        return {'message': f'Notes added to set {set_dict.exercise_name}, {set_dict.set_number}'}, 201

@workout_ns.route('/<string:workout_id>/<int:set_order>/delete_notes')
class DeleteNotesFromSet(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', notes_success),
        404: ('Not Found', notes_failure),
    })
    def delete(self, workout_id, set_order):
        """Delete notes from a set in a workout"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout
        
        set_dict = next((set for set in workout.set_dicts_list if set.set_order == set_order), None)
        if not set_dict:
            return {'error': 'Set not found'}, 404
        
        set_dict.delete_notes()
        workout.save()
        return {'message': f'Notes deleted from set {set_dict.exercise_name}, {set_dict.set_number}'}, 200 