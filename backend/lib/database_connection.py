import os
from mongoengine import connect, disconnect

def initialize_db(db_name="HyPrOps", alias="default"):
    """
    Initialize the MongoDB connection using an environment variable for the URI.
    """
    # Use MONGO_URI if provided, otherwise default to localhost settings
    mongo_uri = os.getenv("MONGO_URI", f"mongodb://localhost:27017/{db_name}")
    connect(alias=alias, host=mongo_uri, uuidRepresentation="standard")
    print(f"Connected to MongoDB database: {db_name} (URI: {mongo_uri})")

def close_db(alias="default"):
    """
    Disconnect from the MongoDB connection.
    """
    disconnect(alias=alias)
    print("Disconnected from MongoDB database.")