from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict, Counter
import re

class ClusteringService:
    def __init__(self, eps: float = 0.3, min_samples: int = 2):
        self.eps = eps
        self.min_samples = min_samples
    
    def cluster_feedbacks(self, feedbacks: List[Dict[str, Any]]) -> Dict[int, List[Dict]]:
        """Cluster similar feedbacks using DBSCAN"""
        if not feedbacks:
            return {}
        
        # Extract embeddings
        embeddings = []
        valid_feedbacks = []
        
        for fb in feedbacks:
            if fb.get('embedding'):
                embeddings.append(fb['embedding'])
                valid_feedbacks.append(fb)
        
        if len(embeddings) < 2:
            return {0: valid_feedbacks}
        
        # Perform clustering
        embeddings_array = np.array(embeddings)
        clustering = DBSCAN(
            eps=self.eps,
            min_samples=self.min_samples,
            metric='cosine'
        ).fit(embeddings_array)
        
        # Group by cluster
        clusters = defaultdict(list)
        for idx, label in enumerate(clustering.labels_):
            clusters[int(label)].append(valid_feedbacks[idx])
        
        return dict(clusters)
    
    def find_cluster_keywords(self, cluster_feedbacks: List[Dict]) -> List[str]:
        """Extract common keywords from a cluster"""
        all_text = " ".join([
            f.get('content', '') + " " + f.get('title', '')
            for f in cluster_feedbacks
        ]).lower()
        
        # Simple keyword extraction (can be enhanced with TF-IDF)
        words = re.findall(r'\b[a-z]{3,}\b', all_text)
        
        # Filter common words
        stop_words = {
            'the', 'and', 'for', 'not', 'but', 'app', 'this', 
            'that', 'with', 'from', 'are', 'was', 'were', 'been'
        }
        words = [w for w in words if w not in stop_words]
        
        # Get most common
        counter = Counter(words)
        return [word for word, count in counter.most_common(10)]
    
    def generate_cluster_title(self, keywords: List[str], category: str) -> str:
        """Generate a descriptive title for a cluster"""
        if not keywords:
            return f"{category.title()} Issue"
        
        # Take top 3 keywords
        top_keywords = keywords[:3]
        return " ".join([w.title() for w in top_keywords]) + " Problem"
    
    def calculate_cluster_severity(self, cluster_feedbacks: List[Dict]) -> str:
        """Calculate severity based on ratings and sentiment"""
        if not cluster_feedbacks:
            return "minor"
        
        # Count negative sentiments
        negative_count = sum(
            1 for f in cluster_feedbacks 
            if f.get('sentiment') == 'negative'
        )
        negative_ratio = negative_count / len(cluster_feedbacks)
        
        # Check ratings
        ratings = [f.get('rating', 3) for f in cluster_feedbacks if f.get('rating')]
        avg_rating = sum(ratings) / len(ratings) if ratings else 3
        
        # Severity logic
        if negative_ratio > 0.7 and avg_rating < 2:
            return "critical"
        elif negative_ratio > 0.5 or avg_rating < 3:
            return "major"
        else:
            return "minor"
    
    def detect_affected_segments(self, cluster_feedbacks: List[Dict]) -> Dict[str, List[str]]:
        """Detect which user segments are affected"""
        segments = {
            'platforms': [],
            'versions': [],
            'regions': [],
            'devices': []
        }
        
        for fb in cluster_feedbacks:
            if fb.get('platform'):
                segments['platforms'].append(fb['platform'])
            
            if fb.get('app_version'):
                segments['versions'].append(fb['app_version'])
            
            if fb.get('region'):
                segments['regions'].append(fb['region'])
            
            device_info = fb.get('device_info', {})
            if device_info.get('model'):
                segments['devices'].append(device_info['model'])
        
        # Get unique and most common
        return {
            key: list(set(values)) if values else []
            for key, values in segments.items()
        }
    
    def calculate_trend(
        self, 
        current_count: int, 
        previous_count: int
    ) -> str:
        """Calculate trend based on count changes"""
        if previous_count == 0:
            return "increasing" if current_count > 0 else "stable"
        
        change_ratio = (current_count - previous_count) / previous_count
        
        if change_ratio > 0.2:
            return "increasing"
        elif change_ratio < -0.5:
            return "decreasing"
        elif current_count == 0:
            return "resolved"
        else:
            return "stable"