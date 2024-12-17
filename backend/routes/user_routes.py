from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from lib.utilities.api_functions import tuple_checker, get_credentials
from mongoengine import NotUniqueError
from models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['POST'])
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
    return jsonify({'message' : user_list}), 200
    
    