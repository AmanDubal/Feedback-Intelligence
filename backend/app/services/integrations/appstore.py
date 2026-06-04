"""
Generic Integration Service Template
Use this as a template for integrating with any feedback source
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GenericIntegrationService:
    """
    Generic integration service for any feedback source
    Can be extended for specific platforms (email, Slack, CSV, API, etc.)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize generic integration service
        
        Args:
            config: Configuration dictionary for the integration
        """
        self.config = config
        self.source_name = config.get('source_name', 'generic')
        self.source_type = config.get('source_type', 'custom')
        logger.info(f"Initialized {self.source_name} ({self.source_type}) integration")
    
    async def fetch_feedback(
        self,
        limit: int = 100,
        offset: int = 0,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Fetch feedback from the integrated source
        Override in subclasses for specific implementations
        
        Args:
            limit: Number of feedback items to fetch
            offset: Pagination offset
            **kwargs: Additional parameters
            
        Returns:
            List of feedback items
        """
        logger.info(f"Fetching feedback from {self.source_name}")
        return []
    
    async def send_feedback(self, feedback: Dict[str, Any]) -> bool:
        """
        Send feedback back to the source (if supported)
        
        Args:
            feedback: Feedback item to send
            
        Returns:
            Success status
        """
        logger.info(f"Sending feedback to {self.source_name}")
        return False
    
    def validate_config(self) -> bool:
        """
        Validate integration configuration
        
        Returns:
            True if valid, False otherwise
        """
        return bool(self.source_name and self.source_type)
    
    def get_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return {
            "source": self.source_name,
            "type": self.source_type,
            "configured": self.validate_config(),
            "timestamp": datetime.now().isoformat()
        }

        
        payload = {
            'iss': self.issuer_id,
            'exp': int(expiry.timestamp()),
            'aud': 'appstoreconnect-v1'
        }
        
        token = jwt.encode(
            payload,
            self.private_key,
            algorithm='ES256',
            headers={'kid': self.key_id, 'typ': 'JWT'}
        )
        
        self.access_token = token
        self.token_expiry = expiry
        return token
    
    async def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers for API requests"""
        # Generate new token if expired or not exists
        if (not self.access_token or 
            not self.token_expiry or
            datetime.utcnow() >= self.token_expiry):
            token = self._generate_jwt()
        else:
            token = self.access_token
        
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    async def fetch_reviews(
        self,
        max_results: int = 1000,
        days_back: int = 90
    ) -> List[Dict[str, Any]]:
        """
        Fetch reviews from Apple App Store
        
        Args:
            max_results: Maximum number of reviews to fetch
            days_back: How many days back to fetch reviews
            
        Returns:
            List of review dictionaries
        """
        reviews = []
        headers = await self._get_headers()
        
        # Date filter for recent reviews
        start_date = (datetime.utcnow() - timedelta(days=days_back)).isoformat()
        
        try:
            async with httpx.AsyncClient() as client:
                # Get app information
                url = f"{self.API_BASE_URL}/apps/{self.app_id}/customerReviews"
                params = {
                    'limit': min(200, max_results),
                    'sort': '-createdDate',
                    'filter[createdDate]': f'{start_date}'
                }
                
                page_token = None
                
                while len(reviews) < max_results:
                    if page_token:
                        params['pageToken'] = page_token
                    
                    response = await client.get(
                        url,
                        headers=headers,
                        params=params
                    )
                    
                    if response.status_code != 200:
                        logger.error(
                            f"Error fetching reviews: {response.status_code} - "
                            f"{response.text}"
                        )
                        break
                    
                    data = response.json()
                    
                    if 'data' not in data:
                        break
                    
                    for review in data['data']:
                        reviews.append({
                            'id': review.get('id'),
                            'content': review.get('attributes', {}).get('body', ''),
                            'title': review.get('attributes', {}).get('title', ''),
                            'rating': review.get('attributes', {}).get('rating', 0),
                            'source': 'app_store',
                            'platform': 'iOS',
                            'version': review.get('attributes', {}).get(
                                'appVersionString', ''
                            ),
                            'device': self._extract_device_info(review),
                            'region': review.get('attributes', {}).get(
                                'territory', ''
                            ),
                            'created_at': review.get('attributes', {}).get(
                                'createdDate', ''
                            ),
                            'updated_at': datetime.utcnow().isoformat(),
                            'author': review.get('attributes', {}).get(
                                'reviewerName', 'Anonymous'
                            ),
                            'is_edited': review.get('attributes', {}).get(
                                'isEdited', False
                            ),
                        })
                    
                    # Check for pagination
                    page_token = data.get('pageToken')
                    if not page_token or len(reviews) >= max_results:
                        break
                    
                    # Be respectful to API rate limits
                    await asyncio.sleep(0.5)
            
            logger.info(f"Fetched {len(reviews)} reviews from App Store")
            return reviews[:max_results]
            
        except Exception as e:
            logger.error(f"Error fetching App Store reviews: {e}")
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
        all_reviews = await self.fetch_reviews(
            max_results=max_results * 2
        )
        
        filtered_reviews = [
            r for r in all_reviews
            if min_rating <= r.get('rating', 0) <= max_rating
        ]
        
        return filtered_reviews[:max_results]
    
    async def get_review_stats(self) -> Dict[str, Any]:
        """
        Get aggregate review statistics from App Store
        
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
                    [r.get('created_at', '') for r in reviews],
                    default=''
                )
            }
            
        except Exception as e:
            logger.error(f"Error getting review stats: {e}")
            return {'error': str(e)}
    
    def _extract_device_info(self, review: Dict) -> Optional[str]:
        """Extract device information from review"""
        try:
            device_mapping = {
                'iphone': 'iPhone',
                'ipad': 'iPad',
                'ipod': 'iPod',
                'mac': 'Mac',
            }
            
            # Parse device info if available
            # This is a simplified extraction; actual structure may vary
            attributes = review.get('attributes', {})
            
            # Try to extract from any available device field
            for key, value in device_mapping.items():
                if key.lower() in str(attributes).lower():
                    return value
            
            return 'iOS Device'
        except:
            return None
    
    async def get_app_metadata(self) -> Dict[str, Any]:
        """
        Get basic app metadata from App Store Connect
        
        Returns:
            Dictionary with app information
        """
        try:
            headers = await self._get_headers()
            
            async with httpx.AsyncClient() as client:
                url = f"{self.API_BASE_URL}/apps/{self.app_id}"
                
                response = await client.get(url, headers=headers)
                
                if response.status_code != 200:
                    logger.error(f"Error fetching app metadata: {response.text}")
                    return {}
                
                data = response.json()
                app_data = data.get('data', {})
                
                return {
                    'id': app_data.get('id'),
                    'name': app_data.get('attributes', {}).get('name', ''),
                    'bundle_id': app_data.get('attributes', {}).get('bundleId', ''),
                    'version': app_data.get('attributes', {}).get('version', ''),
                }
                
        except Exception as e:
            logger.error(f"Error getting app metadata: {e}")
            return {}