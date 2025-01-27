from flask import Flask, jsonify, send_from_directory, request
from lib.database_connection import initialize_db
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from routes.restx_models import auth_ns, user_ns, workout_ns
from flask_restx import Api
from datetime import timedelta

# ✅ Explicitly load .env from the root directory
dotenv_path = find_dotenv("../.env")  # Adjust path if needed
load_dotenv(dotenv_path)

# ✅ Debugging: Check if .env is loaded correctly
print(f"Loaded .env from: {dotenv_path if dotenv_path else 'Not Found'}")

# ✅ Check FLASK_ENV and DEBUG values
FLASK_ENV = os.getenv("FLASK_ENV", "production").strip().lower()
DEBUG_MODE = os.getenv("DEBUG", "False").strip().lower() == "true"

# ✅ Absolute Path to React Build Folder
FRONTEND_DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend/dist")

if not os.path.exists(FRONTEND_DIST_DIR):
    raise RuntimeError(f"⚠️ ERROR: Frontend build directory not found: {FRONTEND_DIST_DIR}")

print(f"🚀 Serving frontend from: {FRONTEND_DIST_DIR}")

def create_app():
    app = Flask(
        __name__,
        static_folder=FRONTEND_DIST_DIR,
        static_url_path=""  
    )

    api = Api(
        app,
        version='3.1',
        title='HyPrOps Workout Tracker API',
        description='API for managing workout tracking',
        doc="/api/docs"
    )

    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)
    JWTManager(app)

    # ✅ Ensure MongoDB URI is properly formatted
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/HyPrOps").strip()
    initialize_db(MONGO_URI)

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(user_ns, path='/user')
    api.add_namespace(workout_ns, path='/workouts')

    @app.route("/")
    def serve_root():
        return send_from_directory(FRONTEND_DIST_DIR, "index.html")

    @app.route('/assets/<path:path>')
    def serve_assets(path):
        return send_from_directory(os.path.join(FRONTEND_DIST_DIR, "assets"), path)

    @app.route("/auth/<path:path>")
    @app.route("/user/<path:path>")
    @app.route("/workouts/<path:path>")
    def serve_api_routes(path):
        return jsonify({"error": "API endpoint not found"}), 404

    @app.errorhandler(404)
    def serve_react(_):
        print(f"🔹 Serving React index.html for a 404 route")
        return send_from_directory(FRONTEND_DIST_DIR, "index.html")

    return app

def main():
    app = create_app()
    port = int(os.environ.get("PORT", 10000))  # Default port

    print(f"🔍 Running in {FLASK_ENV.upper()} mode | Debug: {DEBUG_MODE}")

    app.run(host="0.0.0.0", port=port, debug=DEBUG_MODE)

if __name__ == '__main__':
    main()
