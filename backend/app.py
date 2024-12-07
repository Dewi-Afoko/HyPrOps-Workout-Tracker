from flask import Flask, jsonify, request
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from models.user import User
from models.workout import Workout
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
import os
from mongoengine.errors import NotUniqueError

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

        username = data.get('username')
        password = data.get('password')

        if username == None:
            return jsonify({'error': 'Username not provided'}), 400
        if password == None:
            return jsonify({'error': 'Password not provided'}), 400
        
        else:
            try:
                user = User(username=data['username'], password=data['password'])
                user.hash_password()
                return jsonify({'message' : f'{user.username} successfully registered!'}), 201
            
            except NotUniqueError:
                return jsonify({'error' : 'Username unavailable'}), 409
            
    @app.route('/login', methods=['POST'])
    def login():

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if username == None:
            return jsonify({'error': 'Username not provided'}), 400
        if password == None:
            return jsonify({'error': 'Password not provided'}), 400
        
        else:
            user = User.objects(username=username).first()
            if not user or not check_password_hash(user.password, password):
                return jsonify({'error' : 'Invalid login credentials'}), 401
            
            access_token = create_access_token(identity=username)
            return jsonify({
                'message' : f'Login successful, welcome {username}',
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
        username = get_jwt_identity()
        user = User.objects(username=username).first()
        if not user:
            return jsonify({'error' : 'User not found'})
        
        workout = Workout(user_id=user.id, workout_name=data['workout_name'])

        user.add_workout(workout)
        user.save()

        return jsonify({'message' : f'{workout.workout_name} created by {username}'}), 201
        





    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()