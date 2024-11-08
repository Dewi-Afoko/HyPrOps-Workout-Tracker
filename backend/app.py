from flask import Flask, request, jsonify
from lib.database_connection import initialize_db
from models.user import User
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo
from bson import ObjectId
import os
from dotenv import load_dotenv
from mongoengine.errors import NotUniqueError

load_dotenv()


def create_app():
    app = Flask(__name__)



    # Initialize the MongoDB database
    initialize_db(db_name="HyPrOps")  # Use your actual database name here

    # Home route for testing
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to HyPrOps backend... We finna be cooking!!"})

    # User routes (/users)
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        try:
        # Attempt to create and save the user
            user = User(username=data['username'], password=data['password'])
            user.save()
            return jsonify({"id": str(user.id), "username": user.username}), 201
        except NotUniqueError:
        # Return 400 Bad Request if username already exists
            return jsonify({"error": "Username already exists"}), 400

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.objects()
        if len(users) > 0:
            return jsonify(users=[{"id": str(user.id), "username": user.username} for user in users]), 200
        return jsonify({'error': 'No users found!'}), 400

    # Workout routes (/workouts)

    @app.route('/workouts/<user_id>', methods=['GET'])
    def my_workouts(user_id):
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        workouts = Workout.objects(user_id=user.id)
        workouts_list = [workout.to_dict() for workout in workouts]
        return jsonify(workouts_list), 200

    @app.route('/workouts/<user_id>', methods=['POST'])
    def create_workout(user_id):
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        workout = Workout(user_id=user.id)
        workout.save()
        user.workout_list.append(workout)
        user.save()

        return jsonify({"user_id": str(user.id), "workout_id": str(workout.id)}), 201

    @app.route('/workouts/<user_id>/<workout_id>/add_exercise', methods=['POST'])
    def create_workout_exercise_info(user_id, workout_id):
        workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        data = request.get_json() # Only requirement is exercise name

        for entry in workout['exercise_list']:
            if data['exercise_name'] in entry['exercise_name']:
                return jsonify({"error" : "Exercise already exists, try adding details!"}), 418
        
        details = WorkoutExerciseInfo(exercise_name = data['exercise_name'])
        workout.add_exercise(details)
        return jsonify({"workout id": str(workout.id), "exercise added": str(details.exercise_name)}), 201

    @app.route('/workouts/<user_id>/<workout_id>/add_details', methods=['PATCH'])
    def add_details_to_exercise_info(user_id, workout_id):
        workout = Workout.objects(user_id=user_id, id=ObjectId(workout_id)).first()
        if not workout:
            return jsonify({"error": "Workout not found"}), 404
        data = request.get_json()

    # Payload logic for empty fields
        response_payload = {}
        for entry in workout['exercise_list']:
            if data['exercise_name'] in entry['exercise_name']: # Exercise name required to identify where to add these values
                if "reps" in data:
                    response_payload['reps'] = data['reps']
                    entry.add_set(data['reps'])
                if 'loading' in data:
                    response_payload['loading'] = data['loading']
                    entry.set_loading(data['loading'])
                if 'rest' in data:
                    response_payload['rest'] = data['rest']
                    entry.set_rest_period(data['rest'])
                if 'notes' in data:
                    response_payload['notes'] = data['notes']
                    entry.add_performance_notes(data['notes'])
                workout.save()
                return jsonify(response_payload), 201
        else:
                return jsonify({"error" : "Exercise not found!"}), 418
        
        
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)