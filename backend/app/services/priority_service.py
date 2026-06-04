from typing import Dict, List, Any
from datetime import datetime, timedelta

class PriorityService:
    
    SEVERITY_WEIGHTS = {
        "critical": 10,
        "major": 5,
        "minor": 1
    }
    
    TREND_WEIGHTS = {
        "increasing": 2.0,
        "stable": 1.0,
        "decreasing": 0.5,
        "resolved": 0.1
    }
    
    def calculate_priority_score(self, issue: Dict[str, Any]) -> float:
        """Calculate priority score for an issue"""
        # Base score from complaint count
        complaint_score = issue.get('complaint_count', 0)
        
        # Severity multiplier
        severity = issue.get('severity', 'minor')
        severity_multiplier = self.SEVERITY_WEIGHTS.get(severity, 1)
        
        # Trend multiplier
        trend = issue.get('trend', 'stable')
        trend_multiplier = self.TREND_WEIGHTS.get(trend, 1.0)
        
        # Affected users weight
        affected_users = issue.get('affected_users', 0)
        user_weight = min(affected_users / 100, 5)  # Cap at 5x
        
        # Recency bonus (issues seen recently get higher priority)
        last_seen = issue.get('last_seen')
        recency_bonus = 1.0
        if last_seen:
            days_ago = (datetime.utcnow() - last_seen).days
            recency_bonus = max(1.0, 3.0 - (days_ago / 7))  # Decays over weeks
        
        # Calculate final score
        score = (
            complaint_score * 
            severity_multiplier * 
            trend_multiplier * 
            (1 + user_weight) * 
            recency_bonus
        )
        
        return round(score, 2)
    
    def assign_priority(self, score: float, severity: str) -> str:
        """Assign priority label based on score and severity"""
        if severity == "critical" or score > 100:
            return "immediate"
        elif score > 30 or severity == "major":
            return "next_sprint"
        else:
            return "low"
    
    def rank_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank issues by priority score"""
        # Calculate scores
        for issue in issues:
            issue['priority_score'] = self.calculate_priority_score(issue)
            issue['priority'] = self.assign_priority(
                issue['priority_score'],
                issue.get('severity', 'minor')
            )
        
        # Sort by score descending
        ranked = sorted(
            issues,
            key=lambda x: x['priority_score'],
            reverse=True
        )
        
        return ranked
    
    def get_top_priorities(
        self, 
        issues: List[Dict[str, Any]], 
        limit: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get top priority issues grouped by priority level"""
        ranked = self.rank_issues(issues)
        
        priorities = {
            "immediate": [],
            "next_sprint": [],
            "low": []
        }
        
        for issue in ranked[:limit]:
            priority = issue.get('priority', 'low')
            priorities[priority].append(issue)
        
        return priorities
    
    def calculate_complaint_percentage(
        self, 
        issue_count: int, 
        total_feedbacks: int
    ) -> float:
        """Calculate what percentage of total complaints this issue represents"""
        if total_feedbacks == 0:
            return 0.0
        return round((issue_count / total_feedbacks) * 100, 1)
    
    def should_create_ticket(self, issue: Dict[str, Any]) -> bool:
        """Determine if an issue warrants automatic ticket creation"""
        severity = issue.get('severity', 'minor')
        priority = issue.get('priority', 'low')
        complaint_count = issue.get('complaint_count', 0)
        trend = issue.get('trend', 'stable')
        
        # Create ticket if:
        # 1. Critical severity
        # 2. Immediate priority
        # 3. Major severity with increasing trend
        # 4. More than 20 complaints
        
        if severity == "critical":
            return True
        
        if priority == "immediate":
            return True
        
        if severity == "major" and trend == "increasing":
            return True
        
        if complaint_count > 20:
            return True
        
        return False