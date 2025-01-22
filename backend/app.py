from flask import Flask, send_from_directory, request, jsonify
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from routes.restx_models import auth_ns, user_ns, workout_ns
from flask_restx import Api
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

def create_app():
    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        template_folder=STATIC_DIR
    )

    api = Api(
        app,
        version='3.1',
        title='HyPrOps Workout Tracker API',
        description='API for managing workout tracking',
        doc='/api/docs'  # ✅ Keeps Swagger UI working
    )

    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)
    JWTManager(app)

    initialize_db(db_name="HyPrOps")

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(user_ns, path='/user')
    api.add_namespace(workout_ns, path='/workouts')

    # ✅ Serve `index.html` for the base route `/`
    @app.route("/")
    def serve_root():
        print(f"Serving index.html from {STATIC_DIR}")  # Debug log
        return send_from_directory(STATIC_DIR, "index.html")

    # ✅ Serve static files properly
    @app.route("/assets/<path:filename>")
    def serve_assets(filename):
        return send_from_directory(os.path.join(STATIC_DIR, "assets"), filename)

    # ✅ Handle all **other frontend routes** by returning `index.html`
    @app.route("/<path:path>")
    def serve_react_routes(path):
        # 🔹 If the requested file exists in static folder, serve it (JS, CSS, images, etc.)
        requested_file = os.path.join(STATIC_DIR, path)
        if os.path.exists(requested_file) and not os.path.isdir(requested_file):
            return send_from_directory(STATIC_DIR, path)

        # 🔹 Otherwise, assume it's a React route & serve `index.html`
        print(f"React route triggered, serving index.html for {path}")  # Debugging
        return send_from_directory(STATIC_DIR, "index.html")

    # ✅ Health Check Endpoint (Optional)
    @app.route("/health")
    def health_check():
        return jsonify({"status": "OK", "message": "Backend is running"}), 200

    return app

def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == '__main__':
    main()
