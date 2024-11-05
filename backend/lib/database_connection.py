
from mongoengine import connect, disconnect

def initialize_db(db_name="HyPrOps", host="localhost", port=27017, username=None, password=None, alias="default"):
    """
    Initialize the MongoDB connection.
    """
    connect(
        db=db_name,
        host=host,
        port=port,
        username=username,
        password=password,
        authentication_source="admin" if username else None,
        alias=alias,
        uuidRepresentation="standard"  # Set uuidRepresentation to suppress deprecation warning
    )
    print(f"Connected to MongoDB database: {db_name}")

def close_db(alias="default"):
    """
    Disconnect from the MongoDB connection.
    """
    disconnect(alias=alias)
    print("Disconnected from MongoDB database.")
