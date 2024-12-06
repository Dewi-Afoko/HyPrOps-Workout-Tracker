from flask import Flask, jsonify, request
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from models.user import User
from flask_jwt_extended import JWTManager
import os
from mongoengine.errors import NotUniqueError

load_dotenv()

#TODO: Routes separated into blueprints

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
    
# User Database Routes

    @app.route('/user', methods=['POST'])
    def register():
        data = request.get_json()
        if 'username' not in data.keys():
            return jsonify({'error': 'Username not provided'}), 400
        if 'password' not in data.keys():
            return jsonify({'error': 'Password not provided'}), 400
        else:
            try:
                user = User(username=data['username'], password=data['password'])
                user.hash_password()
                return jsonify({'message' : f'{user.username} successfully registered!'}), 201
            except NotUniqueError:
                return jsonify({'error' : 'Username unavailable'}), 409





    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()