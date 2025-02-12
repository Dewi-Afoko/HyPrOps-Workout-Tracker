from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import User, Workout, SetDicts
from datetime import datetime
from lib.utilities.helper_functions import find_set_dicts, find_single_set_dict, find_single_workout, find_user_from_jwt, find_user_workouts_list, workouts_as_dict, check_for_error
from mongoengine import ValidationError
from flask_restx import Resource
from .restx_models import workout_ns, workout_get_success, workout_get_failure, single_workout_success, single_workout_failure, create_workout_request, create_workout_success, create_workout_failure, notes_request, notes_success, notes_failure, mark_complete_success, add_set_request, add_set_success, add_set_failure, mark_set_complete_success, delete_set_failure, delete_set_success, edit_workout_failure, edit_workout_request, edit_workout_success, edit_set_failure, edit_set_request, edit_set_success, delete_workout_failure, delete_workout_success,duplicated_set_failure,duplicated_set_success,duplicated_workout_failure,duplicated_workout_success



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
    
@workout_ns.route('/<string:workout_id>/delete_set/<int:set_order>')
class DeleteSetFromWorkout(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', delete_set_success),
        404: ('Not Found', delete_set_failure),
        400: ('Bad Request', delete_set_failure),
    })
    def delete(self, workout_id, set_order):
        """Delete a set from a workout by its set_order"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout

        try:
            workout.delete_set_dict(set_order)
            return {'message': f'Set {set_order} successfully deleted from workout {workout.workout_name}'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Failed to delete set: {str(e)}'}, 500


@workout_ns.route('/<string:workout_id>/edit_details')
class EditWorkoutDetails(Resource):
    @jwt_required()
    @workout_ns.expect(edit_workout_request)
    @workout_ns.doc(responses={
        200: ('Success', edit_workout_success),
        400: ('Bad Request', edit_workout_failure),
        404: ('Not Found', edit_workout_failure),
    })
    def patch(self, workout_id):
        """Edit workout details"""
        data = request.get_json()
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout

        try:
            workout.edit_details(
                name=data.get('name'),
                date=data.get('date'),
                user_weight=data.get('user_weight'),
                sleep_score=data.get('sleep_score'),
                sleep_quality=data.get('sleep_quality'),
            )
            return {'message': f'Workout {workout.workout_name} details updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Failed to update workout details: {str(e)}'}, 400

@workout_ns.route('/<string:workout_id>/edit_set')
class EditSet(Resource):
    @jwt_required()
    @workout_ns.expect(edit_set_request)
    @workout_ns.doc(responses={
        200: ('Success', edit_set_success),
        400: ('Bad Request', edit_set_failure),
        404: ('Not Found', edit_set_failure),
    })
    def patch(self, workout_id):
        """Edit details of a set in a workout"""
        data = request.get_json()
        user = find_user_from_jwt()
        if check_for_error(user):
            return user
        
        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout

        set_order = data.get('set_order')
        if set_order is None:
            return {'error': 'Set order is required'}, 400

        try:
            editable_data = {key: value for key, value in data.items() if key != 'set_order'}
            response = workout.edit_set(set_order, **editable_data)
            return response, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except KeyError as e:
            return {'error': f"Invalid field: {str(e)}"}, 400
        except Exception as e:
            return {'error': f"Failed to update set: {str(e)}"}, 400


@workout_ns.route('/<string:workout_id>')
class DeleteWorkout(Resource):
    @jwt_required()
    @workout_ns.doc(responses={
        200: ('Success', delete_workout_success),
        404: ('Not Found', delete_workout_failure),
    })
    def delete(self, workout_id):
        """Delete a workout by ID"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user

        workout = Workout.objects(id=workout_id, user_id=user.id).first()
        if not workout:
            return {"error": "Workout not found"}, 404

        workout.delete()
        return {"message": f"Workout {workout_id} deleted successfully"}, 200

@workout_ns.route('/<string:workout_id>/duplicate')
class DuplicateWorkout(Resource):
    @jwt_required()
    @workout_ns.response(201, 'Workout duplicated successfully', duplicated_workout_success)
    @workout_ns.response(404, 'Workout not found', duplicated_workout_failure)
    @workout_ns.response(500, 'Internal server error', duplicated_workout_failure)
    def post(self, workout_id):
        user = find_user_from_jwt()
        if check_for_error(user):
            return user

        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout

        try:
            # Create a new Workout by copying the existing one
            duplicate_workout = Workout(
                user_id=workout.user_id,
                workout_name=f"{workout.workout_name} (Copy)",
                date=datetime.now(),
                notes=workout.notes,
                set_dicts_list=[
                    SetDicts(
                        exercise_name=set_dict.exercise_name,
                        set_type=set_dict.set_type,
                        reps=set_dict.reps,
                        loading=set_dict.loading,
                        focus=set_dict.focus,
                        rest=set_dict.rest,
                        notes=set_dict.notes,
                    )
                    for set_dict in workout.set_dicts_list
                ],
            )
            duplicate_workout.format_workout()
            duplicate_workout.save()
            return {"message": "Workout duplicated successfully", "workout": duplicate_workout.to_dict()}, 201
        except Exception as e:
            return {"error": f"Failed to duplicate workout: {str(e)}"}, 500
        

@workout_ns.route('/<string:workout_id>/<int:set_order>/duplicate_set')
class DuplicateSet(Resource):
    @jwt_required()
    @workout_ns.response(200, 'Success', duplicated_set_success)
    @workout_ns.response(404, 'Not Found', duplicated_set_failure)
    @workout_ns.response(500, 'Internal Server Error', duplicated_set_failure)
    def post(self, workout_id, set_order):
        """Duplicate a set within a workout"""
        user = find_user_from_jwt()
        if check_for_error(user):
            return user

        workout = find_single_workout(workout_id)
        if check_for_error(workout):
            return workout

        # Find the set to duplicate
        set_to_duplicate = next(
            (s for s in workout.set_dicts_list if s.set_order == set_order), None
        )

        if not set_to_duplicate:
            return {'error': 'Set not found'}, 404

        try:
            # Duplicate the set
            duplicated_set = set_to_duplicate.duplicate()

            # Add to the workout's set_dicts_list
            workout.set_dicts_list.append(duplicated_set)

            # Recalculate the set orders and numbers
            workout.format_workout()

            # Save the workout (and its associated sets)
            workout.save()

            return {
                'message': 'Set duplicated successfully',
                'set': duplicated_set.to_dict()  # Ensure `to_dict` is implemented
            }, 200

        except Exception as e:
            return {'error': f'Failed to duplicate set: {str(e)}'}, 500
