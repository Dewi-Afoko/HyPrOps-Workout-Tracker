from flask import Blueprint, request, jsonify
from models.workout import Workout
from models.user import User
from bson import ObjectId

workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/workouts/<user_id>', methods=['GET'])
def my_workouts(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    workouts = Workout.objects(user_id=user.id)
    workouts_list = [workout.to_dict() for workout in workouts]
    return jsonify(workouts_list), 200

@workout_bp.route('/workouts/<user_id>', methods=['POST'])
def create_workout(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    workout = Workout(user_id=user.id)
    workout.save()
    user.workout_list.append(workout)
    user.save()

    return jsonify({"user_id": str(user.id), "workout_id": str(workout.id)}), 201
