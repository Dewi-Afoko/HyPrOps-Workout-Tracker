from flask_restx import Namespace, fields

# Define Namespace
workout_ns = Namespace('workout', description='All actions related to workouts')

# Model for successful GET workouts
workout_get_success = workout_ns.model('WorkoutGetSuccess', {
    'message' : fields.String(description="Confirmation request was successful"),
    'workouts' : fields.List(fields.String, description="A list of all user's workouts"),
})

# Model for GET workouts failure
workout_get_failure = workout_ns.model('WorkoutGetFailure', {
    'error' : fields.String(description="An error message as no workouts were found"),
})

# Registration Request Model
user_registration_request = workout_ns.model('UserRegistrationRequest', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

# Model for successful registration
user_registration_success = workout_ns.model('UserRegistrationSuccess', {
    'message': fields.String(description='A message confirming registration of user by username'),
})

# Model for registration failure
user_registration_error = workout_ns.model('UserRegistrationError', {
    'error': fields.String(description='Error message telling user why registration failed'),
})
