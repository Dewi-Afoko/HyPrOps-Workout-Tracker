from flask_restx import Namespace, Resource, fields, marshal

# Define Namespace
auth_ns = Namespace('auth', description='Login and authentication functions')

# Define request model
user_login_request = auth_ns.model('UserLoginRequest', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

# Model for successful login
user_login_success = auth_ns.model('UserLoginSuccess', {
    'token': fields.String(description='The authentication token'),
    'user': fields.Raw(description='User as dict'),
    'message': fields.String(description='A messaging welcoming the user by username'),
})

# Model for failed login
user_login_error = auth_ns.model('UserLoginError', {
    'error': fields.String(description='An error message for invalid login credentials'),
})