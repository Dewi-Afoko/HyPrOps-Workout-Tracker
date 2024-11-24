from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models.user import User

token_bp = Blueprint("auth", __name__, url_prefix="/token")

@token_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Validate user
    user = User.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Generate JWT
    access_token = create_access_token(identity=str(user.username))
    return jsonify({'token': access_token, "advice": "It's dangerous to go alone, take this with you *hands over a JWT*", 'user_id': str(user.id)}), 200

@token_bp.route('/token_check', methods=['GET'])
@jwt_required()
def token_check():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome, user {current_user}!", "advice": "It's dangerous to go alone, take this with you *hands over a JWT*"}), 200
