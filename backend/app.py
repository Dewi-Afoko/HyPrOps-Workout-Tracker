from flask import Flask, jsonify
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from routes import user_bp, auth_bp, workouts_bp

load_dotenv()

#TODO: Decide whether the enumerate functions should be simplified in the models.

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWTManager(app)
    app.config["TESTING"] = True
    # Initialize the database
    initialize_db(db_name="HyPrOps")

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(workouts_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to HyPrOps backend... We finna be cooking!!"})

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()