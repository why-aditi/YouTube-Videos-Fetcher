import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_url)
        db.database = db.client[settings.database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Create indexes for optimization
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")


async def create_indexes():
    """Create database indexes for optimization"""
    try:
        videos_collection = db.database.videos
        
        # Create indexes
        await videos_collection.create_index("video_id", unique=True)
        await videos_collection.create_index([("published_at", -1)])  # Descending order for latest first
        await videos_collection.create_index("channel_id")
        await videos_collection.create_index("title")
        await videos_collection.create_index("tags")
        await videos_collection.create_index([("created_at", -1)])
        
        # Compound indexes for common queries
        await videos_collection.create_index([
            ("published_at", -1),
            ("channel_id", 1)
        ])
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db.database

