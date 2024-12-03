from lib.database_connection import DatabaseConnection

# Run this file to reset your database using the seeds

connection = DatabaseConnection(test_mode=False)
connection.connect()

# Add your own seed lines below...
# E.g.connection.seed("seeds/your_seed.sql")


connection.seed("seeds/UserWorkoutExercise.sql")

# Add your own seed lines below...
# E.g.connection.seed("seeds/your_seed.sql")

# run python seed_dev_database.py instead of psql -h 127.0.0.1 {database_name} < {file_containing_sql}`