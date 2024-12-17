from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models.user import User
from lib.utilities.api_functions import tuple_checker, get_credentials

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    credentials = get_credentials(data)
    if tuple_checker(credentials):
        return credentials
    else:
        user = User.objects(username=credentials['username']).first()
        if not user:
            return jsonify({'error' : 'User not found'}), 401
        
        if not check_password_hash(user.password, credentials['password']):
            return jsonify({'error' : 'Invalid login credentials'}), 401
        
        access_token = create_access_token(identity=credentials['username'])
        return jsonify({
            'message' : f'Login successful, welcome {credentials["username"]}',
            'token' : access_token}), 200