"""
Platform-Independent Feedback Ingestion Service
Supports multiple feedback sources: CSV, API, Email, Manual input, etc.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class FeedbackSourceType(str, Enum):
    """Supported feedback source types"""
    CSV = "csv"
    JSON = "json"
    API = "api"
    EMAIL = "email"
    MANUAL = "manual"
    WEBHOOK = "webhook"
    OTHER = "other"

class FeedbackIngestService:
    """
    Platform-independent feedback ingestion service
    Handles feedback from any source (not limited to app stores)
    """
    
    def __init__(self):
        """Initialize feedback ingestion service"""
        self.sources: Dict[str, Dict[str, Any]] = {}
        logger.info("Initialized platform-independent feedback ingestion service")
    
    def register_source(
        self,
        source_name: str,
        source_type: FeedbackSourceType,
        config: Dict[str, Any] = None
    ) -> bool:
        """
        Register a new feedback source
        
        Args:
            source_name: Name of the source
            source_type: Type of source
            config: Optional configuration
            
        Returns:
            Success status
        """
        self.sources[source_name] = {
            "type": source_type,
            "config": config or {},
            "created_at": datetime.now(),
            "total_feedback": 0
        }
        logger.info(f"Registered feedback source: {source_name} ({source_type})")
        return True
    
    async def ingest_feedback(
        self,
        source_name: str,
        feedback_items: List[Dict[str, Any]]
    ) -> int:
        """
        Ingest feedback items from a source
        
        Args:
            source_name: Source identifier
            feedback_items: List of feedback items
            
        Returns:
            Number of items ingested
        """
        if source_name not in self.sources:
            logger.warning(f"Unknown source: {source_name}")
            return 0
        
        self.sources[source_name]["total_feedback"] += len(feedback_items)
        logger.info(f"Ingested {len(feedback_items)} items from {source_name}")
        return len(feedback_items)
    
    def list_sources(self) -> List[Dict[str, Any]]:
        """Get all registered feedback sources"""
        return [
            {
                "name": name,
                "type": source["type"].value,
                "created_at": source["created_at"].isoformat(),
                "total_feedback": source["total_feedback"]
            }
            for name, source in self.sources.items()
        ]
    
    def get_source_stats(self, source_name: str) -> Dict[str, Any]:
        """Get statistics for a specific source"""
        if source_name not in self.sources:
            return {}
        
        source = self.sources[source_name]
        return {
            "name": source_name,
            "type": source["type"].value,
            "total_feedback": source["total_feedback"],
            "created_at": source["created_at"].isoformat()
        }

            
        Returns:
            List of review dictionaries
        """
        reviews = []
        page_token = None
        
        try:
            while len(reviews) < max_results:
                request = self.service.reviews().list(
                    packageName=self.package_name,
                    maxResults=min(250, max_results - len(reviews)),
                    pageToken=page_token
                )
                
                response = await asyncio.to_thread(request.execute)
                
                if 'reviews' not in response:
                    break
                
                for review in response['reviews']:
                    reviews.append({
                        'id': review.get('reviewId'),
                        'content': review.get('comments', [{}])[0].get('userComment', {}).get('text', ''),
                        'title': '',  # Play Store doesn't provide titles
                        'rating': review.get('comments', [{}])[0].get('userComment', {}).get('starRating', 0),
                        'source': 'play_store',
                        'platform': self._extract_platform(review),
                        'version': review.get('comments', [{}])[0].get('userComment', {}).get('appVersionCode', ''),
                        'device': self._extract_device(review),
                        'region': review.get('comments', [{}])[0].get('userComment', {}).get('deviceMetadata', {}).get('deviceClass', ''),
                        'created_at': review.get('comments', [{}])[0].get('userComment', {}).get('lastModified', {}).get('seconds', 0),
                        'updated_at': datetime.utcnow().isoformat(),
                        'author': review.get('authorName', 'Anonymous'),
                        'thumbs_up_count': review.get('comments', [{}])[0].get('userComment', {}).get('thumbsUpCount', 0),
                    })
                
                page_token = response.get('pageToken')
                if not page_token:
                    break
                
                # Be respectful to the API
                await asyncio.sleep(1)
            
            logger.info(f"Fetched {len(reviews)} reviews from Play Store")
            return reviews
            
        except Exception as e:
            logger.error(f"Error fetching Play Store reviews: {e}")
            raise
    
    async def fetch_reviews_by_rating(
        self,
        min_rating: int = 1,
        max_rating: int = 5,
        max_results: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Fetch reviews filtered by rating
        
        Args:
            min_rating: Minimum star rating (1-5)
            max_rating: Maximum star rating (1-5)
            max_results: Maximum number of reviews
            
        Returns:
            List of review dictionaries
        """
        all_reviews = await self.fetch_reviews(max_results=max_results * 2)
        
        filtered_reviews = [
            r for r in all_reviews
            if min_rating <= r.get('rating', 0) <= max_rating
        ]
        
        return filtered_reviews[:max_results]
    
    def _extract_platform(self, review: Dict) -> str:
        """Extract Android version/platform from review"""
        try:
            os_version = review.get('comments', [{}])[0].get(
                'userComment', {}
            ).get('deviceMetadata', {}).get('platformVersion', '')
            return f"Android {os_version}" if os_version else "Android"
        except:
            return "Android"
    
    def _extract_device(self, review: Dict) -> str:
        """Extract device model from review"""
        try:
            device = review.get('comments', [{}])[0].get(
                'userComment', {}
            ).get('deviceMetadata', {}).get('device', '')
            return device if device else None
        except:
            return None
    
    async def reply_to_review(
        self,
        review_id: str,
        reply_text: str
    ) -> bool:
        """
        Reply to a review (developer response)
        
        Args:
            review_id: The review ID to reply to
            reply_text: The response text
            
        Returns:
            True if successful
        """
        try:
            request = self.service.reviews().reply(
                packageName=self.package_name,
                reviewId=review_id,
                body={'replyText': reply_text}
            )
            
            await asyncio.to_thread(request.execute)
            logger.info(f"Replied to review {review_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error replying to review: {e}")
            return False
    
    async def get_review_stats(self) -> Dict[str, Any]:
        """
        Get aggregate review statistics
        
        Returns:
            Dictionary with stats like average rating, total reviews, etc.
        """
        try:
            reviews = await self.fetch_reviews(max_results=100)
            
            if not reviews:
                return {'error': 'No reviews found'}
            
            ratings = [r.get('rating', 0) for r in reviews]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            return {
                'total_reviews': len(reviews),
                'average_rating': round(avg_rating, 2),
                'rating_distribution': {
                    1: sum(1 for r in ratings if r == 1),
                    2: sum(1 for r in ratings if r == 2),
                    3: sum(1 for r in ratings if r == 3),
                    4: sum(1 for r in ratings if r == 4),
                    5: sum(1 for r in ratings if r == 5),
                },
                'latest_review_date': max(
                    [r.get('created_at', 0) for r in reviews],
                    default=0
                )
            }
            
        except Exception as e:
            logger.error(f"Error getting review stats: {e}")
            return {'error': str(e)}