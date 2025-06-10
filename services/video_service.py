from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import DESCENDING
from models.video import VideoModel, VideoFilter, VideoResponse
from core.database import get_database
import logging

logger = logging.getLogger(__name__)


class VideoService:
    def __init__(self):
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.collection = None

    def _ensure_connection(self):
        """Ensure database connection is available"""
        if self.db is None:
            self.db = get_database()
            self.collection = self.db.videos

    async def create_video(self, video_data: dict) -> VideoModel:
        """Create a new video record"""
        self._ensure_connection()
        try:
            video_data["created_at"] = datetime.utcnow()
            video_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.insert_one(video_data)
            video_data["_id"] = result.inserted_id
            
            return VideoModel(**video_data)
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise

    async def get_video_by_id(self, video_id: str) -> Optional[VideoModel]:
        """Get video by YouTube video ID"""
        self._ensure_connection()
        try:
            video_data = await self.collection.find_one({"video_id": video_id})
            if video_data:
                return VideoModel(**video_data)
            return None
        except Exception as e:
            logger.error(f"Error getting video by ID: {e}")
            raise

    async def update_video(self, video_id: str, update_data: dict) -> Optional[VideoModel]:
        """Update video record"""
        self._ensure_connection()
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.find_one_and_update(
                {"video_id": video_id},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                return VideoModel(**result)
            return None
        except Exception as e:
            logger.error(f"Error updating video: {e}")
            raise

    async def upsert_video(self, video_data: dict) -> VideoModel:
        """Insert or update video record"""
        self._ensure_connection()
        try:
            video_id = video_data.get("video_id")
            existing_video = await self.get_video_by_id(video_id)
            
            if existing_video:
                # Update existing video
                update_data = {k: v for k, v in video_data.items() if k != "video_id"}
                return await self.update_video(video_id, update_data)
            else:
                # Create new video
                return await self.create_video(video_data)
        except Exception as e:
            logger.error(f"Error upserting video: {e}")
            raise

    async def get_videos_paginated(
        self,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[VideoFilter] = None
    ) -> VideoResponse:
        """Get paginated videos with optional filters"""
        self._ensure_connection()
        try:
            # Build query
            query = {}
            
            if filters:
                if filters.search:
                    query["$or"] = [
                        {"title": {"$regex": filters.search, "$options": "i"}},
                        {"description": {"$regex": filters.search, "$options": "i"}},
                        {"channel_title": {"$regex": filters.search, "$options": "i"}}
                    ]
                
                if filters.channel_id:
                    query["channel_id"] = filters.channel_id
                
                if filters.published_after or filters.published_before:
                    date_query = {}
                    if filters.published_after:
                        date_query["$gte"] = filters.published_after
                    if filters.published_before:
                        date_query["$lte"] = filters.published_before
                    query["published_at"] = date_query

            # Calculate pagination
            skip = (page - 1) * per_page
            
            # Get total count
            total = await self.collection.count_documents(query)
            
            # Get videos
            cursor = self.collection.find(query).sort("published_at", DESCENDING).skip(skip).limit(per_page)
            videos_data = await cursor.to_list(length=per_page)
            
            videos = [VideoModel(**video_data) for video_data in videos_data]
            
            total_pages = (total + per_page - 1) // per_page
            
            return VideoResponse(
                videos=videos,
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )
            
        except Exception as e:
            logger.error(f"Error getting paginated videos: {e}")
            raise

    async def get_latest_videos(self, limit: int = 10) -> List[VideoModel]:
        """Get latest videos"""
        self._ensure_connection()
        try:
            cursor = self.collection.find().sort("published_at", DESCENDING).limit(limit)
            videos_data = await cursor.to_list(length=limit)
            return [VideoModel(**video_data) for video_data in videos_data]
        except Exception as e:
            logger.error(f"Error getting latest videos: {e}")
            raise

    async def delete_video(self, video_id: str) -> bool:
        """Delete video by YouTube video ID"""
        self._ensure_connection()
        try:
            result = await self.collection.delete_one({"video_id": video_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting video: {e}")
            raise

    async def get_video_count(self) -> int:
        """Get total video count"""
        self._ensure_connection()
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            logger.error(f"Error getting video count: {e}")
            raise


# Global video service instance
video_service = VideoService()

