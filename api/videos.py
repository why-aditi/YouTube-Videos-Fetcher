from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from datetime import datetime
from models.video import VideoResponse, VideoFilter
from services.video_service import video_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/", response_model=VideoResponse)
async def get_videos(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in title, description, or channel"),
    channel_id: Optional[str] = Query(None, description="Filter by channel ID"),
    published_after: Optional[datetime] = Query(None, description="Filter videos published after this date"),
    published_before: Optional[datetime] = Query(None, description="Filter videos published before this date"),
):
    """
    Get paginated videos sorted by published datetime (descending)
    
    - **page**: Page number (starts from 1)
    - **per_page**: Number of videos per page (max 100)
    - **search**: Search term for title, description, or channel name
    - **channel_id**: Filter by specific channel ID
    - **published_after**: Filter videos published after this date (ISO format)
    - **published_before**: Filter videos published before this date (ISO format)
    """
    try:
        filters = VideoFilter(
            search=search,
            channel_id=channel_id,
            published_after=published_after,
            published_before=published_before
        )
        
        result = await video_service.get_videos_paginated(
            page=page,
            per_page=per_page,
            filters=filters
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/latest")
async def get_latest_videos(
    limit: int = Query(10, ge=1, le=50, description="Number of latest videos to return")
):
    """
    Get the latest videos (quick endpoint for recent videos)
    
    - **limit**: Number of latest videos to return (max 50)
    """
    try:
        videos = await video_service.get_latest_videos(limit=limit)
        return {"videos": videos, "count": len(videos)}
        
    except Exception as e:
        logger.error(f"Error getting latest videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats")
async def get_video_stats():
    """
    Get basic statistics about stored videos
    """
    try:
        total_count = await video_service.get_video_count()
        latest_videos = await video_service.get_latest_videos(limit=1)
        
        stats = {
            "total_videos": total_count,
            "latest_video": latest_videos[0] if latest_videos else None
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting video stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{video_id}")
async def get_video_by_id(video_id: str):
    """
    Get a specific video by its YouTube video ID
    
    - **video_id**: YouTube video ID
    """
    try:
        video = await video_service.get_video_by_id(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return video
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

