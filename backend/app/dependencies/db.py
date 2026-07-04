from backend.app.core.database import get_database

def get_db():
    """
    Dependency that yields the active MongoDB database instance.
    Can be used with FastAPI's Depends() to perform DB injections.
    """
    return get_database()
