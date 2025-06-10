import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional
from services.youtube_service import youtube_client
from services.video_service import video_service
from core.config import settings

logger = logging.getLogger(__name__)


class BackgroundTaskService:
    def __init__(self):
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
        self.last_fetch_time: Optional[datetime] = None
        self.fetch_count = 0
        self.error_count = 0

    async def start_background_fetching(self):
        """Start the background video fetching task"""
        if self.is_running:
            logger.warning("Background fetching is already running")
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._fetch_videos_loop())
        logger.info("Started background video fetching")

    async def stop_background_fetching(self):
        """Stop the background video fetching task"""
        if not self.is_running:
            logger.warning("Background fetching is not running")
            return
        
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped background video fetching")

    async def _fetch_videos_loop(self):
        """Main loop for fetching videos"""
        logger.info(f"Starting video fetch loop with {settings.fetch_interval}s interval")
        
        while self.is_running:
            try:
                await self._fetch_and_store_videos()
                self.fetch_count += 1
                self.last_fetch_time = datetime.utcnow()
                
                # Wait for the specified interval
                await asyncio.sleep(settings.fetch_interval)
                
            except asyncio.CancelledError:
                logger.info("Background fetching cancelled")
                break
            except Exception as e:
                self.error_count += 1
                logger.error(f"Error in background fetching: {e}")
                # Wait a bit longer on error to avoid rapid retries
                await asyncio.sleep(min(settings.fetch_interval * 2, 60))

    async def _fetch_and_store_videos(self):
        """Fetch videos from YouTube and store them in database"""
        try:
            # Calculate the time window for fetching new videos
            # Fetch videos published in the last hour to ensure we don't miss any
            published_after = datetime.utcnow() - timedelta(hours=1)
            
            logger.info(f"Fetching videos for query: '{settings.search_query}'")
            
            # Fetch videos from YouTube
            videos = await youtube_client.search_videos(
                query=settings.search_query,
                max_results=settings.max_results_per_request,
                published_after=published_after,
                order="date"
            )
            
            if not videos:
                logger.info("No new videos found")
                return
            
            # Store videos in database
            stored_count = 0
            updated_count = 0
            
            for video_data in videos:
                try:
                    existing_video = await video_service.get_video_by_id(video_data['video_id'])
                    
                    if existing_video:
                        # Update existing video with latest data
                        await video_service.update_video(video_data['video_id'], video_data)
                        updated_count += 1
                    else:
                        # Store new video
                        await video_service.create_video(video_data)
                        stored_count += 1
                        
                except Exception as e:
                    logger.error(f"Error storing video {video_data.get('video_id', 'unknown')}: {e}")
            
            logger.info(f"Processed {len(videos)} videos: {stored_count} new, {updated_count} updated")
            
        except Exception as e:
            logger.error(f"Error fetching and storing videos: {e}")
            raise

    async def force_fetch(self) -> dict:
        """Force an immediate fetch (for testing/manual trigger)"""
        try:
            start_time = datetime.utcnow()
            await self._fetch_and_store_videos()
            end_time = datetime.utcnow()
            
            return {
                "success": True,
                "message": "Manual fetch completed successfully",
                "duration": (end_time - start_time).total_seconds(),
                "timestamp": end_time.isoformat()
            }
        except Exception as e:
            logger.error(f"Error in manual fetch: {e}")
            return {
                "success": False,
                "message": f"Manual fetch failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_status(self) -> dict:
        """Get current status of background fetching"""
        return {
            "is_running": self.is_running,
            "last_fetch_time": self.last_fetch_time.isoformat() if self.last_fetch_time else None,
            "fetch_count": self.fetch_count,
            "error_count": self.error_count,
            "fetch_interval": settings.fetch_interval,
            "search_query": settings.search_query,
            "max_results_per_request": settings.max_results_per_request
        }


# Global background task service instance
background_service = BackgroundTaskService()

