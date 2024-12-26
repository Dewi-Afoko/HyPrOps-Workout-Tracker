from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from lib.utilities.api_functions import tuple_checker, get_credentials, find_user_from_jwt
from mongoengine import NotUniqueError, ValidationError
from models import User
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def register():
        data = request.get_json()

        credentials = get_credentials(data)
        if tuple_checker(credentials):
            return credentials
        try:
            user = User(username=credentials['username'], password=credentials['password'])
            user.hash_password()
            return jsonify({'message' : f'{user.username} successfully registered!'}), 201
            
        except NotUniqueError:
            return jsonify({'error' : 'Username unavailable'}), 409
        
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_list = [User.to_dict() for User in User.objects()]
    if len(user_list) > 1:
        return jsonify({'error' : 'No users found!'}), 404
    return jsonify({'message' : user_list}), 200
    
@user_bp.route('/users/add_personal_data', methods=['POST'])
@jwt_required()
def add_personal_data():
    data = request.get_json()
    user = find_user_from_jwt()
    try:
        if 'dob' in data.keys():
            dob = datetime.strptime(data.get('dob'), '%Y/%m/%d')
            personal_data = PersonalData(name=data.get('name'), dob=dob, height=data.get('height'), weight=data.get('weight'))
        else:
            personal_data = PersonalData(name=data.get('name'), height=data.get('height'), weight=data.get('weight'))
        user.add_personal_data(personal_data)
        user.save()
        print(f'{personal_data.to_dict()}')
    except ValidationError:
        return jsonify({"error" : "Failed to create Personal Data"}), 400

    return jsonify({"message" : "Personal data updated"}), 201