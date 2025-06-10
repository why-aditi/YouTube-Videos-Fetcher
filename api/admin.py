from fastapi import APIRouter, HTTPException
from services.background_service import background_service
from services.youtube_service import youtube_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/status")
async def get_system_status():
    """
    Get overall system status including background tasks and API quota
    """
    try:
        background_status = background_service.get_status()
        quota_status = youtube_client.get_quota_status()
        
        return {
            "background_service": background_status,
            "youtube_api": quota_status,
            "system": {
                "status": "healthy" if background_status["is_running"] else "stopped"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/background/start")
async def start_background_fetching():
    """
    Start the background video fetching service
    """
    try:
        await background_service.start_background_fetching()
        return {"message": "Background fetching started successfully"}
        
    except Exception as e:
        logger.error(f"Error starting background fetching: {e}")
        raise HTTPException(status_code=500, detail="Failed to start background fetching")


@router.post("/background/stop")
async def stop_background_fetching():
    """
    Stop the background video fetching service
    """
    try:
        await background_service.stop_background_fetching()
        return {"message": "Background fetching stopped successfully"}
        
    except Exception as e:
        logger.error(f"Error stopping background fetching: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop background fetching")


@router.post("/background/force-fetch")
async def force_fetch_videos():
    """
    Force an immediate video fetch (for testing/manual trigger)
    """
    try:
        result = await background_service.force_fetch()
        return result
        
    except Exception as e:
        logger.error(f"Error in force fetch: {e}")
        raise HTTPException(status_code=500, detail="Failed to force fetch videos")


@router.get("/background/status")
async def get_background_status():
    """
    Get detailed status of the background fetching service
    """
    try:
        return background_service.get_status()
        
    except Exception as e:
        logger.error(f"Error getting background status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/youtube/quota")
async def get_youtube_quota_status():
    """
    Get YouTube API quota status for all configured keys
    """
    try:
        return youtube_client.get_quota_status()
        
    except Exception as e:
        logger.error(f"Error getting YouTube quota status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

