from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from core.config import settings
from core.database import connect_to_mongo, close_mongo_connection
from api.videos import router as videos_router
from api.admin import router as admin_router
from services.background_service import background_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting YouTube Video Fetcher API")
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        logger.info("Connected to MongoDB")
        
        # Start background video fetching
        await background_service.start_background_fetching()
        logger.info("Started background video fetching")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down YouTube Video Fetcher API")
    
    try:
        # Stop background tasks
        await background_service.stop_background_fetching()
        logger.info("Stopped background video fetching")
        
        # Close database connection
        await close_mongo_connection()
        logger.info("Closed MongoDB connection")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="YouTube Video Fetcher API",
    description="API for fetching and storing YouTube videos with background processing",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(videos_router)
app.include_router(admin_router)

# Serve static files (for React dashboard)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "YouTube Video Fetcher API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "videos": "/api/videos",
            "admin": "/api/admin",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if background service is running
        bg_status = background_service.get_status()
        
        return {
            "status": "healthy",
            "background_service": bg_status["is_running"],
            "timestamp": bg_status.get("last_fetch_time"),
            "fetch_count": bg_status["fetch_count"]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )

