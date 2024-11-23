import os
from mongoengine import connect, disconnect


def initialize_db(db_name=None, alias="default"):
    # Check APP_ENV and set db_name if not provided
    if os.environ.get("APP_ENV") == "test":
        db_name = "test_mongodb"
    else:
        db_name = db_name or "HyPrOps"  # Default to the primary database

    print(f"Connecting to database: {db_name}")  # Debugging log


    connect(
        db=db_name,
        alias=alias,
        uuidRepresentation="standard"  # Set to 'standard' to avoid deprecation warning
    )

def close_db(alias="default"):
    """
    Disconnect from the MongoDB connection.
    """
    disconnect(alias=alias)
    print("Disconnected from MongoDB database.")