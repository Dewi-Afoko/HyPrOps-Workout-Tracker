# from flask import Blueprint, request, jsonify
# from models.workout import Workout
# from models.user import User
# from flask_jwt_extended import jwt_required

# workout_bp = Blueprint('workout_bp', __name__)

# @workout_bp.route('/workouts/<user_id>', methods=['GET'])
# @jwt_required()
# def my_workouts(user_id):
#     user = User.objects(id=user_id).first()
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     workouts = Workout.objects(user_id=user.id)
#     workouts_list = [workout.to_dict() for workout in workouts]
#     return jsonify(workouts_list), 200

# @workout_bp.route('/workouts/<user_id>', methods=['POST'])
# @jwt_required()
# def create_workout(user_id):
#     user = User.objects(id=user_id).first()
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     workout = Workout(user_id=user.id)
#     workout.save()
#     user.workout_list.append(workout)
#     user.save()

#     return jsonify({"user_id": str(user.id), "workout_id": str(workout.id)}), 201

# @workout_bp.route('/workouts/<user_id>/<workout_id>', methods=['PATCH'])
# @jwt_required()
# def complete_workout(user_id, workout_id):
#     user = User.objects(id=user_id).first()
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     workout = Workout.objects(id=workout_id).first()
#     print(f'{workout =}')
#     workout.mark_complete()

#     return jsonify({"message": "completion status updated", "workout_id": str(workout.complete)}), 200

