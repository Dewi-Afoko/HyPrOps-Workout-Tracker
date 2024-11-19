from flask import Flask, jsonify
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from routes.user_routes import user_bp
from routes.workout_routes import workout_bp
from routes.workout_details_routes import workout_details_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize the database
    initialize_db(db_name="HyPrOps")

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(workout_details_bp)

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to HyPrOps backend... We finna be cooking!!"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)