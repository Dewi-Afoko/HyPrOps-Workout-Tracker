from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from lib.utilities.helper_functions import get_credentials, find_user_from_jwt
from mongoengine import NotUniqueError, ValidationError
from models import User
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def register():
        data = request.get_json()

        credentials, status_code = get_credentials(data)
        if status_code == 400:
            return credentials, status_code

        try:
            user = User(username=credentials['username'], password=credentials['password'])
            user.hash_password()
            return {'message' : f'{user.username} successfully registered!'}, 201
            
        except NotUniqueError:
            return jsonify({'error' : 'Username unavailable'}), 409
        
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_list = [User.to_dict() for User in User.objects()]
    if len(user_list) > 1:
        return jsonify({'error' : 'No users found!'}), 404
    return jsonify({'message' : user_list}), 200
    
@user_bp.route('/users/update_personal_data', methods=['PATCH'])
@jwt_required()
def update_personal_data():
    data = request.get_json()
    payload = {**data}
    user = find_user_from_jwt()
    try: 
        user.update_personal_details(**payload)
    except ValidationError:
        return jsonify({"error" : "Failed to create Personal Data"}), 400

    return jsonify({"message" : "Personal data updated"}), 201