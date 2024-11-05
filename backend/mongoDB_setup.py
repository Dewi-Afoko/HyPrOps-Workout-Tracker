from mongoengine import connect, disconnect
from models.user import User
from models.workout import Workout
from models.workout_exercise_info import WorkoutExerciseInfo

def initialize_db(db_name="HyPrOps", host="localhost", port=27017, username=None, password=None):
    """
    Initialize the MongoDB connection.
    """
    connect(
        db=db_name,
        host=host,
        port=port,
        username=username,
        password=password,
        authentication_source="admin" if username else None
    )
    print(f"Connected to MongoDB database: {db_name}")

def clear_database():
    """
    Clear all collections in the connected MongoDB database.
    Useful for resetting the database in a development environment.
    """
    try:
        for model in [User, Workout, WorkoutExerciseInfo]:
            model.drop_collection()
        print("Cleared all collections in the database.")
    except AttributeError as e:
        print(f"Error clearing database: {e}")

def seed_data():
    """
    Seed the database with initial data for development/testing purposes.
    """
    # Create and save a new user
    user = User(username="sample_user", password="hashedpassword")
    user.save()

    # Create a workout associated with the user's ID
    workout = Workout(user_id=user)
    
    # Create a WorkoutExerciseInfo instance and add it to the workout's exercise list
    exercise_info = WorkoutExerciseInfo(exercise_name="Push-ups")
    exercise_info.reps = [10, 12, 15]
    exercise_info.loading = [0.0, 0.0, 0.0]
    exercise_info.rest = [60, 60, 90]
    exercise_info.performance_notes = ["Felt strong", "Need improvement", "Good form"]
    
    # Append the exercise info to workout's exercise list
    workout.exercise_list.append(exercise_info)
    workout.save()  # Save after adding exercises

    # Append the workout to the user's workout list and save the user
    user.workout_list.append(workout)
    user.save()
    
    print("Database seeded with sample data.")

def setup_mongodb(dev_mode=True):
    """
    Setup MongoDB: Connect, clear (if in dev mode), and optionally seed data.
    """
    initialize_db()
    if dev_mode:
        clear_database()
        seed_data()

if __name__ == "__main__":
    setup_mongodb(dev_mode=True)
