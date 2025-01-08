from flask_restx import Namespace, fields

# Define Namespace
user_ns = Namespace('user', description='Creation and editing of user documents')

# Model for successful GET users
user_get_success = user_ns.model('UserGetSuccess', {
    'message' : fields.List(fields.Raw, description="A list of all registered users as objects"),
})

# Model for GET users failure
user_get_failure = user_ns.model('UserGetFailure', {
    'error' : fields.String(description="An error message as no users were found"),
})

# Registration Request Model
user_registration_request = user_ns.model('UserRegistrationRequest', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

# Model for successful registration
user_registration_success = user_ns.model('UserRegistrationSuccess', {
    'message': fields.String(description='A message confirming registration of user by username'),
})

# Model for registration failure
user_registration_error = user_ns.model('UserRegistrationError', {
    'error': fields.String(description='Error message telling user why registration failed'),
})

# Update User Request Model
user_update_request = user_ns.model('UserUpdateRequest', {
    'name': fields.String(required=False, description='The username of the user'),
    'dob': fields.String(required=False, description='The date of birth of the user in YYYY/MM/DD format'),
    'height': fields.Float(required=False, description='The height of the user'),
    'weight': fields.Float(required=False, description='The weight of the user'),
})

# Model for successful user update
user_update_success = user_ns.model('UserUpdateSuccess', {
    'message' : fields.String(description='Message confirming specified details were updated') 
})

# Model for user update failure
user_update_failure = user_ns.model('UserUpdateFailure', {
    'error' : fields.String(description='Error for failure to update details') 
})

# Successful response model for user details
user_details_success = user_ns.model('UserDetailsSuccess', {
    'id': fields.String(description="The user's unique ID"),
    'name': fields.String(description="The user's name", example="John Doe"),
    'dob': fields.String(description="The user's date of birth", example="1990-01-01"),
    'height': fields.Float(description="The user's height in cm", example=180.0),
    'weight': fields.Float(description="The user's weight in kg", example=75.0),
})

# Error response model
user_details_error = user_ns.model('UserDetailsError', {
    'error': fields.String(description="Error message", example="User not found"),
})