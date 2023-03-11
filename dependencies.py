from models.database import db_conn_handle


async def get_db():
    """
    Generates a session maker object for querying the database
    """
    yield db_conn_handle
