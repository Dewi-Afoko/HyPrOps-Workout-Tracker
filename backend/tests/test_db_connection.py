import pytest
from mongoengine import get_connection, disconnect
from mongoengine.connection import ConnectionFailure

def test_database_connection_initialization_and_disconnection():
    from lib.database_connection import initialize_db, close_db

    # Use a unique alias to avoid conflicts with session-wide connection
    alias = "test_connection"
    
    # Ensure no existing connection with this alias
    disconnect(alias=alias)
    
    # Initialize the database connection with the unique alias
    initialize_db(db_name="test_mongodb_temp", alias=alias)
    
    # Verify that the connection was established
    connection = get_connection(alias=alias)
    assert connection is not None

    # Disconnect and verify that the connection is closed
    close_db(alias=alias)
    
    # Trying to access the connection after disconnection should raise an error
    with pytest.raises(ConnectionFailure):
        get_connection(alias=alias)
