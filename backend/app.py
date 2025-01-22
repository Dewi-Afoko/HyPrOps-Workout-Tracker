from flask import Flask, jsonify, send_from_directory
from lib.database_connection import initialize_db
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from routes.restx_models import auth_ns, user_ns, workout_ns
from flask_restx import Api
from datetime import timedelta

load_dotenv()

# Ensure Flask serves the correct frontend folder
FRONTEND_DIST_DIR = "/Users/dewi/Desktop/programming/projects/Fullstack_HyPrOps/frontend/dist"

# 🔹 Debugging: Ensure frontend folder exists
if not os.path.exists(FRONTEND_DIST_DIR):
    raise RuntimeError(f"⚠️ ERROR: Frontend build directory not found: {FRONTEND_DIST_DIR}")

print(f"🚀 Serving frontend from: {FRONTEND_DIST_DIR}")

def create_app():
    app = Flask(__name__, static_folder=FRONTEND_DIST_DIR, static_url_path="")

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
    app.config["TESTING"] = True
    initialize_db(db_name="HyPrOps")

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(user_ns, path='/user')
    api.add_namespace(workout_ns, path='/workouts')

    # ✅ Ensure API routes still return JSON
    @app.route("/auth/<path:path>")
    @app.route("/user/<path:path>")
    @app.route("/workouts/<path:path>")
    def serve_api_routes(path):
        print(f"🔹 API request received: {path}")
        return jsonify({"error": "API endpoint not found"}), 404

    # ✅ Serve Static Assets (JS, CSS, Images)
    @app.route('/assets/<path:path>')
    def serve_assets(path):
        print(f"🔹 Serving asset: {path}")
        return send_from_directory(os.path.join(FRONTEND_DIST_DIR, "assets"), path)

    # ✅ Serve React Frontend for ALL Non-API Routes
    @app.errorhandler(404)
    def serve_react(_):
        """
        Ensures React Router works:
        - API routes are handled by Flask
        - Everything else serves `index.html` so React Router can take over
        """
        print(f"🔹 Serving React index.html for a 404 route")
        return send_from_directory(FRONTEND_DIST_DIR, "index.html")

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
