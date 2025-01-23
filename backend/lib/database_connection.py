from mongoengine import connect, disconnect
import os
from urllib.parse import urlparse

def initialize_db(uri):
    """ Initialize MongoDB connection using MongoEngine """

    # ✅ Extract the database name from the URI
    parsed_uri = urlparse(uri)
    db_name = parsed_uri.path.lstrip("/")  # Removes leading "/"

    if not db_name:
        raise ValueError("Database name is missing from MongoDB URI")

    print(f"✅ Connecting to MongoDB: {uri} (Database: {db_name})")

    connect(
        db=db_name,
        host=uri,  # ✅ Full MongoDB URI
        alias="default"
    )


def close_db(alias="default"):
    """
    Disconnect from the MongoDB connection.
    """
    disconnect(alias=alias)
    print("Disconnected from MongoDB database.")