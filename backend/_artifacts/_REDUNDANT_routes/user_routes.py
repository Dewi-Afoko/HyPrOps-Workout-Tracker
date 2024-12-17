# from flask import Blueprint, request, jsonify
# from models.user import User
# from mongoengine.errors import NotUniqueError
# from flask_jwt_extended import jwt_required

# # Ensure the Blueprint name is unique
# user_bp = Blueprint('user_bp', __name__)

# @user_bp.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     try:
#         user = User(username=data['username'], password=data['password'])
#         user.save()
#         return jsonify({"id": str(user.id), "username": user.username}), 201
#     except NotUniqueError:
#         return jsonify({"error": "Username already exists"}), 400

# @user_bp.route('/users', methods=['GET'])
# @jwt_required()
# def get_users():
#     users = User.objects()
#     if not users:
#         return jsonify({'error': 'No users found!'}), 400
#     return jsonify(users=[{"id": str(user.id), "username": user.username} for user in users]), 200

