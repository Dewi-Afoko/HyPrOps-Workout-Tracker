from flask import Flask, jsonify, request
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from models.user import User
from models.set_dicts import SetDicts
from models.workout import Workout
from models.user_stats import UserStats
from models.personal_data import PersonalData
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
import os
from mongoengine.errors import NotUniqueError, ValidationError
from lib.utilities.api_functions import find_user_from_jwt, tuple_checker, get_credentials

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWTManager(app)
    app.config["TESTING"] = True
    # Initialize the database
    initialize_db(db_name="HyPrOps")

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to HyPrOps backend... We finna be cooking!!"})
    




                    ### USER ROUTES ###

    @app.route('/user', methods=['POST'])
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
            
    @app.route('/login', methods=['POST'])
    def login():

        data = request.get_json()

        credentials = get_credentials(data)
        if tuple_checker(credentials):
            return credentials
        else:
            user = User.objects(username=credentials['username']).first()
            if not user or not check_password_hash(user.password, credentials['password']):
                return jsonify({'error' : 'Invalid login credentials'}), 401
            
            access_token = create_access_token(identity=credentials['username'])
            return jsonify({
                'message' : f'Login successful, welcome {credentials["username"]}',
                'token' : access_token}), 200


    """
                                JWT routes
    """       
    
    @app.route('/users', methods=['GET'])
    @jwt_required()
    def get_users():
        user_list = [User.to_dict() for User in User.objects()]
        return jsonify({'message' : user_list}), 200
    
    
                    ### WORKOUT ROUTES ###
    
    @app.route('/workouts', methods=['POST'])
    @jwt_required()
    def create_workout():
        data = request.get_json()
        if 'workout_name' not in data.keys():
            return jsonify({'error' : 'You need to name your workout'}), 400
        user = find_user_from_jwt()
        if tuple_checker(user):
            return user

        workout = Workout(user_id=str(user.id), workout_name=data['workout_name'])

        user.add_workout(workout)

        return jsonify({'message' : f'{workout.workout_name} created by {user.username}'}), 201
        
    @app.route('/workouts', methods=['GET'])
    @jwt_required()
    def get_all_workouts():
        username = get_jwt_identity()
        user = User.objects(username=username).first()
        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        workouts = []
        for workout in user.workout_list:
            workout_dict = workout.to_dict()
            workouts.append(workout_dict)

        if not workouts:
            return jsonify({'error' : 'No workouts found'}), 400

        return jsonify({
        'message': 'Here are your workouts:',
        'workouts': workouts
    }), 200

    @app.route('/workouts/<workout_id>', methods=['GET'])
    @jwt_required()
    def get_single_workout(workout_id):
        username = get_jwt_identity()
        user = User.objects(username=username).first()
        
        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        workout = next((workout.to_dict() for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'No workouts found'}), 400
        
        return jsonify({
        'message': f'Here are the details for workout ID: {workout_id}',
        'workout': workout
    }), 200

    @app.route('/workouts/<workout_id>/add_notes', methods=['PATCH'])
    @jwt_required()
    def add_workout_notes(workout_id):
        data = request.get_json()
        username = get_jwt_identity()
        user = User.objects(username=username).first()

        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'No workouts found'}), 400
        
        workout.add_notes(data.get('notes'))
        user.save()
        return jsonify({'message' : f'{data.get("notes")}: added to workout notes'}), 202
    
    @app.route('/workouts/<workout_id>/delete_note/<note_index>', methods=['DELETE'])
    @jwt_required()
    def delete_workout_note(workout_id, note_index):

        username = get_jwt_identity()
        user = User.objects(username=username).first()

        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'No workouts found'}), 400
        
        workout.delete_note(note_index)
        user.save()

        return jsonify({'message' : 'Note successfully deleted'}), 202

    @app.route('/workouts/<workout_id>/mark_complete', methods=['PATCH'])
    @jwt_required()
    def toggle_workout_complete(workout_id):
        
        username = get_jwt_identity()
        user = User.objects(username=username).first()

        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'No workouts found'}), 400
        
        workout.toggle_complete()
        user.save()
        if workout.complete == True:
            status = "complete"
        elif workout.complete == False:
            status = "incomplete"

        return jsonify({'message' : f'Workout marked as {status}'}), 201
    
    @app.route('/workouts/<workout_id>/add_stats', methods=['PUT'])
    @jwt_required()
    def add_stats_to_workout(workout_id):
        data = request.get_json()
        
        username = get_jwt_identity()
        user = User.objects(username=username).first()

        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'No workouts found'}), 400
        
        if user.personal_data != None:
            personal_data = user.personal_data

        if not personal_data:
            return jsonify({'error' : 'No personal data found'}), 400

        user_stats = UserStats(weight=personal_data, sleep_score=data.get('sleep_score'), sleep_quality=data.get('sleep_quality'), notes=data.get('notes'))

        if not user_stats:
            return jsonify({'error' : 'No personal data found'}), 400

        workout.add_stats(user_stats)
        user.save()

        return jsonify({'message' : 'Stats added to workout'}), 201
    
    

                ### SET DICTS ROUTES ###

    @app.route('/workouts/<workout_id>/add_set', methods=['POST'])
    @jwt_required()
    def add_set_dict(workout_id):

        data = request.get_json()

        if 'exercise_name' not in data.keys():
            return jsonify({'error' : 'You need to specify an exercise'}), 400
        
        username = get_jwt_identity()

        user = User.objects(username=username).first()
        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)


        if not workout:
            return jsonify({'error' : 'Workout not found'}), 400
        
        set_order = (len(workout.set_dicts_list) + 1)
        
        set_number = len([set for set in workout.set_dicts_list if set.exercise_name == data['exercise_name']])

        try:
            set_dict = SetDicts(set_order=set_order, exercise_name=data.get('exercise_name'), set_number=set_number, set_type=data.get('set_type'), reps=data.get('reps'), loading=data.get('loading'), focus=data.get('focus'), rest=data.get('rest'), notes=data.get('notes'))

            workout.add_set_dict(set_dict)
            user.save()

            return jsonify({'message': f'Set info for {set_dict.exercise_name} created and added to {workout.workout_name}'}), 201

        except(ValidationError):
            return jsonify({'error' : 'Failure to create set dictionary'}), 400     
        

    @app.route('/workouts/<workout_id>/<set_order>/mark_complete', methods=['PATCH'])
    @jwt_required()
    def toggle_set_complete(workout_id, set_order):

        username = get_jwt_identity()

        user = User.objects(username=username).first()
        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'Workout not found'}), 400

        set_dict = next((set for set in workout.set_dicts_list if set.set_order == int(set_order)), None)

        set_dict.toggle_complete()
        user.save()
        if set_dict.complete == True:
            return jsonify({'message' : 'Set marked complete'}), 201
        elif set_dict.complete == False:
            return jsonify({'message' : 'Set marked incomplete'}), 201
        

    @app.route('/workouts/<workout_id>/<set_order>/add_notes', methods=['PATCH'])
    @jwt_required()
    def add_notes_to_set(workout_id, set_order):
        data = request.get_json()
        username = get_jwt_identity()

        user = User.objects(username=username).first()
        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'Workout not found'}), 400

        set_dict = next((set for set in workout.set_dicts_list if set.set_order == int(set_order)), None)

        set_dict.add_notes(data.get('notes'))
        user.save()

        return jsonify({'message' : 'Notes added to set'}), 201

    @app.route('/workouts/<workout_id>/<set_order>/delete_notes', methods=['DELETE'])
    @jwt_required()
    def delete_set_notes(workout_id, set_order):
        username = get_jwt_identity()

        user = User.objects(username=username).first()
        if not user:
            return jsonify({'error' : 'User not found'}), 400
        
        
        workout = next((workout for workout in user.workout_list if str(workout.id) == workout_id), None)

        if not workout:
            return jsonify({'error' : 'Workout not found'}), 400

        set_dict = next((set for set in workout.set_dicts_list if set.set_order == int(set_order)), None)

        set_dict.delete_notes()
        user.save()

        return jsonify({'message' : 'Notes deleted'}), 200


    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()