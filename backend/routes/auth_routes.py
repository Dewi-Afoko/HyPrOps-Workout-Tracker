from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models.user import User
from lib.utilities.api_functions import check_for_error, get_credentials
from flask_restx import Namespace, Resource, fields, marshal


auth_ns = Namespace('auth', description='Login and authentication functions')

# Define models
user_login_request = auth_ns.model('UserLoginRequest', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

# Model for successful login
user_login_success = auth_ns.model('UserLoginSuccess', {
    'token': fields.String(description='The authentication token'),
    'message': fields.String(description='A messaging welcoming the user by username'),
})

# Model for failed login
user_login_error = auth_ns.model('UserLoginError', {
    'error': fields.String(description='An error message for invalid login credentials'),
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_login_request)
    @auth_ns.doc(responses={
        200: ('Success', user_login_success),
        400: ('Bad Request', user_login_error),
        401: ('Unauthorized', user_login_error),
    })
    def post(self):

        data = request.get_json()

        credentials, status_code = get_credentials(data)
        if status_code == 400:
            return credentials, status_code

        else:
            user = User.objects(username=credentials['username']).first()
            if not user:
                response = {'error' : 'User not found'}
                return marshal(response, user_login_error), 401
            
            if not check_password_hash(user.password, credentials['password']):
                response = {'error' : 'Invalid login credentials'}
                return marshal(response, user_login_error), 401
            
            access_token = create_access_token(identity=credentials['username'])
            response = {
                'message' : f'Login successful, welcome {credentials["username"]}','token' : access_token}
            return marshal(response, user_login_success), 200
        