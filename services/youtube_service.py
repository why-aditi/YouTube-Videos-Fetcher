import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from core.config import settings

logger = logging.getLogger(__name__)


class YouTubeAPIClient:
    def __init__(self):
        self.api_keys = settings.get_api_keys()
        self.current_key_index = 0
        self.quota_reset_time = {}
        self.quota_exhausted = set()
        
        if not self.api_keys:
            raise ValueError("No YouTube API keys provided")
        
        logger.info(f"Initialized YouTube API client with {len(self.api_keys)} API keys")

    def _get_next_available_key(self) -> Optional[str]:
        """Get the next available API key that hasn't exhausted its quota"""
        now = datetime.utcnow()
        
        # Reset quota for keys that have passed the reset time (24 hours)
        for key in list(self.quota_exhausted):
            if key in self.quota_reset_time:
                if now >= self.quota_reset_time[key]:
                    self.quota_exhausted.discard(key)
                    del self.quota_reset_time[key]
                    logger.info(f"Quota reset for API key ending in ...{key[-4:]}")
        
        # Find next available key
        for i in range(len(self.api_keys)):
            key_index = (self.current_key_index + i) % len(self.api_keys)
            key = self.api_keys[key_index]
            
            if key not in self.quota_exhausted:
                self.current_key_index = key_index
                return key
        
        return None

    def _mark_key_exhausted(self, api_key: str):
        """Mark an API key as quota exhausted"""
        self.quota_exhausted.add(api_key)
        # Set reset time to 24 hours from now
        self.quota_reset_time[api_key] = datetime.utcnow() + timedelta(hours=24)
        logger.warning(f"API key ending in ...{api_key[-4:]} quota exhausted")

    async def search_videos(
        self,
        query: str,
        max_results: int = 50,
        published_after: Optional[datetime] = None,
        order: str = "date"
    ) -> List[Dict[str, Any]]:
        """Search for videos using YouTube Data API v3"""
        api_key = self._get_next_available_key()
        if not api_key:
            raise Exception("All API keys have exhausted their quota")
        
        try:
            # Build YouTube service
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # Prepare search parameters
            search_params = {
                'part': 'id,snippet',
                'q': query,
                'type': 'video',
                'order': order,
                'maxResults': min(max_results, 50),  # API limit is 50
                'regionCode': 'US',
                'relevanceLanguage': 'en'
            }
            
            if published_after:
                search_params['publishedAfter'] = published_after.isoformat() + 'Z'
            
            # Execute search
            search_response = youtube.search().list(**search_params).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            
            if not video_ids:
                return []
            
            # Get detailed video information
            videos_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            videos = []
            for item in videos_response['items']:
                video_data = self._parse_video_data(item)
                videos.append(video_data)
            
            logger.info(f"Successfully fetched {len(videos)} videos using API key ending in ...{api_key[-4:]}")
            return videos
            
        except HttpError as e:
            if e.resp.status == 403 and 'quota' in str(e).lower():
                self._mark_key_exhausted(api_key)
                # Try with next available key
                return await self.search_videos(query, max_results, published_after, order)
            else:
                logger.error(f"YouTube API error: {e}")
                raise
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            raise

    def _parse_video_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse video data from YouTube API response"""
        snippet = item['snippet']
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        # Parse thumbnails
        thumbnails = {}
        for quality, thumbnail in snippet.get('thumbnails', {}).items():
            thumbnails[quality] = {
                'url': thumbnail['url'],
                'width': thumbnail.get('width', 0),
                'height': thumbnail.get('height', 0)
            }
        
        # Parse published date
        published_at = datetime.fromisoformat(
            snippet['publishedAt'].replace('Z', '+00:00')
        ).replace(tzinfo=None)
        
        return {
            'video_id': item['id'],
            'title': snippet['title'],
            'description': snippet['description'],
            'published_at': published_at,
            'channel_id': snippet['channelId'],
            'channel_title': snippet['channelTitle'],
            'thumbnails': thumbnails,
            'duration': content_details.get('duration'),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'tags': snippet.get('tags', []),
            'category_id': snippet.get('categoryId'),
            'language': snippet.get('defaultLanguage')
        }

    async def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 50,
        published_after: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get videos from a specific channel"""
        return await self.search_videos(
            query=f"channel:{channel_id}",
            max_results=max_results,
            published_after=published_after,
            order="date"
        )

    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota status for all API keys"""
        now = datetime.utcnow()
        status = {
            'total_keys': len(self.api_keys),
            'available_keys': len(self.api_keys) - len(self.quota_exhausted),
            'exhausted_keys': len(self.quota_exhausted),
            'current_key_index': self.current_key_index,
            'keys_status': []
        }
        
        for i, key in enumerate(self.api_keys):
            key_status = {
                'index': i,
                'key_suffix': key[-4:],
                'is_exhausted': key in self.quota_exhausted,
                'reset_time': None
            }
            
            if key in self.quota_reset_time:
                key_status['reset_time'] = self.quota_reset_time[key].isoformat()
            
            status['keys_status'].append(key_status)
        
        return status


# Global YouTube API client instance
youtube_client = YouTubeAPIClient()

