from flask_restx import Namespace, fields

# Define Namespace
workout_ns = Namespace('workout', description='All actions related to workouts')

# Shared Models
set_dict_model = workout_ns.model('SetDict', {
    'set_order': fields.Integer(description='Order of the set in the workout'),
    'exercise_name': fields.String(description='Name of the exercise'),
    'set_number': fields.Integer(description='Set number for this exercise'),
    'set_type': fields.String(description='Type of the set'),
    'reps': fields.Integer(description='Number of reps in the set'),
    'loading': fields.Float(description='Loading weight or resistance'),
    'focus': fields.String(description='Focus or goal of the set'),
    'rest': fields.Float(description='Rest period after the set'),
    'notes': fields.String(description='Additional notes for the set'),
    'complete': fields.Boolean(description='Whether the set is complete')
})

# Models for GET workouts
workout_get_success = workout_ns.model('WorkoutGetSuccess', {
    'message': fields.String(description="Confirmation request was successful"),
    'workouts': fields.List(fields.Raw, description="A list of all user's workouts"),
})

workout_get_failure = workout_ns.model('WorkoutGetFailure', {
    'error': fields.String(description="An error message indicating no workouts were found"),
})

# Models for GET single workout
single_workout_success = workout_ns.model('SingleWorkoutSuccess', {
    'message': fields.String(description="Confirmation request was successful"),
    'workout': fields.Raw(description="The details of a single workout"),
})

single_workout_failure = workout_ns.model('SingleWorkoutFailure', {
    'error': fields.String(description="An error message indicating the workout was not found"),
})

# Model for creating a workout
create_workout_request = workout_ns.model('CreateWorkoutRequest', {
    'workout_name': fields.String(required=True, description="The name of the new workout"),
})

create_workout_success = workout_ns.model('CreateWorkoutSuccess', {
    'message': fields.String(description="Confirmation that the workout was created"),
    'workout': fields.Raw(description="The workout object that was created"),
})

create_workout_failure = workout_ns.model('CreateWorkoutFailure', {
    'error': fields.String(description="An error message indicating the workout could not be created"),
})

# Models for adding/deleting notes to/from workout
notes_request = workout_ns.model('NotesRequest', {
    'notes': fields.String(required=True, description="Notes to add or update"),
})

notes_success = workout_ns.model('NotesSuccess', {
    'message': fields.String(description="Confirmation that notes were successfully added or deleted"),
})

notes_failure = workout_ns.model('NotesFailure', {
    'error': fields.String(description="An error message indicating failure to update notes"),
})

# Model for marking workout completion
mark_complete_success = workout_ns.model('MarkCompleteSuccess', {
    'message': fields.String(description="Confirmation that the workout was marked as complete or incomplete"),
})

# Model for adding a set to a workout
add_set_request = workout_ns.model('AddSetRequest', {
    'exercise_name': fields.String(required=True, description="The name of the exercise"),
    'set_type': fields.String(description="Type of the set"),
    'reps': fields.Integer(description="Number of reps in the set"),
    'loading': fields.Float(description="Weight or resistance for the set"),
    'focus': fields.String(description="Focus or goal of the set"),
    'rest': fields.Float(description="Rest time after the set"),
    'notes': fields.String(description="Additional notes for the set"),
})

add_set_success = workout_ns.model('AddSetSuccess', {
    'message': fields.String(description="Confirmation that the set was added to the workout"),
})

add_set_failure = workout_ns.model('AddSetFailure', {
    'error': fields.String(description="An error message indicating the set could not be added"),
})

# Model for marking a set complete
mark_set_complete_success = workout_ns.model('MarkSetCompleteSuccess', {
    'message': fields.String(description="Confirmation that the set was marked as complete or incomplete"),
})

# Response model for successful deletion
delete_set_success = workout_ns.model('DeleteSetSuccess', {
    'message': fields.String(description='Confirmation message that the set was deleted')
})

# Response model for deletion failure
delete_set_failure = workout_ns.model('DeleteSetFailure', {
    'error': fields.String(description='Error message describing the failure')
})

# Model for the request payload
edit_workout_request = workout_ns.model('EditWorkoutRequest', {
    'name': fields.String(required=False, description='The new name for the workout'),
    'date': fields.String(required=False, description='The new date for the workout (format: YYYY-MM-DD)'),
    'user_weight': fields.Float(required=False, description='The user’s weight in kg'),
    'sleep_score': fields.Float(required=False, description='The user’s sleep score'),
    'sleep_quality': fields.String(required=False, description='The user’s sleep quality (e.g., "Good", "Poor")'),
})

# Model for a successful response
edit_workout_success = workout_ns.model('EditWorkoutSuccess', {
    'message': fields.String(description='A message confirming the workout was updated successfully'),
})

# Model for a failure response
edit_workout_failure = workout_ns.model('EditWorkoutFailure', {
    'error': fields.String(description='An error message describing why the update failed'),
})

# Request model for editing a set
edit_set_request = workout_ns.model('EditSetRequest', {
    'set_order': fields.Integer(required=True, description='The order of the set to edit'),
    'exercise_name': fields.String(required=False, description='The new exercise name'),
    'set_type': fields.String(required=False, description='The type of set (e.g., warmup, working, dropset)'),
    'reps': fields.Integer(required=False, description='The number of repetitions'),
    'loading': fields.Float(required=False, description='The loading in kg or weight used'),
    'focus': fields.String(required=False, description='The focus of the set (e.g., form, max load)'),
    'rest': fields.Float(required=False, description='The rest time in seconds'),
    'notes': fields.String(required=False, description='Any additional notes for the set'),
})

# Response model for successful edit
edit_set_success = workout_ns.model('EditSetSuccess', {
    'message': fields.String(description='A message confirming the set was updated successfully'),
})

# Response model for failure
edit_set_failure = workout_ns.model('EditSetFailure', {
    'error': fields.String(description='An error message describing why the update failed'),
})

delete_workout_success = workout_ns.model('DeleteWorkoutSuccess', {
    'message': fields.String(description='Confirmation that the workout was deleted'),
})

delete_workout_failure = workout_ns.model('DeleteWorkoutFailure', {
    'error': fields.String(description='Error message describing why the deletion failed'),
})
