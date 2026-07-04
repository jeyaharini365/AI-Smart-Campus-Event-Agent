import logging
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_connection = Database()

async def connect_to_mongo():
    """Establish connection to MongoDB Atlas."""
    logger.info("Connecting to MongoDB Atlas...")
    db_connection.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db_connection.db = db_connection.client[settings.DATABASE_NAME]
    logger.info("Connected to MongoDB successfully!")

async def close_mongo_connection():
    """Close connection to MongoDB Atlas."""
    logger.info("Closing MongoDB Atlas connection...")
    if db_connection.client:
        db_connection.client.close()
    logger.info("MongoDB connection closed.")

def get_database():
    """Retrieve active MongoDB database instance."""
    if db_connection.db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return db_connection.db
