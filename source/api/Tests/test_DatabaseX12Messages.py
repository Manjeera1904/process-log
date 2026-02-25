from sqlalchemy import create_engine, inspect
import pytest
import os

# Database connection details from environment variables
username = 'sa'
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER', '127.0.0.1')
port = os.getenv('DB_PORT')
database = 'EIProcessLogging'     
 
@pytest.fixture(scope='module')
def db_connection():
    """Fixture to create and yield a database connection."""
    engine = create_engine(f'mssql+pymssql://{username}:{password}@{server}/{database}')
    connection = engine.connect()
    yield connection
    connection.close()

def test_connection_success(db_connection):
    """Test if the connection to the database is successful."""
    assert db_connection is not None, "Connection to the database failed."

@pytest.mark.parametrize("table_name", [
    'X12Messages'
])
def test_table_exists(db_connection, table_name):
    """Test if the specified table exists in the database."""
    inspector = inspect(db_connection)
    tables = inspector.get_table_names()
    
    assert table_name in tables, f"Table {table_name} does not exist in the database."

# Use pytest.mark.parametrize to test multiple columns for multiple tables
@pytest.mark.parametrize("table_name, column_name", [
    ('X12Messages', 'X12MessageId'), 
    ('X12Messages', 'X12InterchangeId'),
    ('X12Messages', 'X12FunctionalGroupId'),
    ('X12Messages', 'X12TransactionSetId'),
    ('X12Messages', 'MessageLevel'),
    ('X12Messages', 'Message'),
    ('X12Messages', 'UpdatedBy'),
    ('X12Messages', 'RowVersion')
])
def test_columns_exist(db_connection, table_name, column_name):
    """Test if specific columns exist in the specified table."""
    inspector = inspect(db_connection)

    columns = inspector.get_columns(table_name)
    existing_column_names = [column['name'] for column in columns]

    assert column_name in existing_column_names, f"Column {column_name} does not exist in the table {table_name}."

if __name__ == "__main__":
    pytest.main()