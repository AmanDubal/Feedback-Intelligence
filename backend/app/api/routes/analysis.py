from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.database import get_db
from app.models.feedback import Feedback
from app.models.issue import Issue, Severity, Priority, Trend
from app.services.clustering_service import ClusteringService
from app.services.priority_service import PriorityService
from app.services.ai_service import AIService

router = APIRouter()
clustering_service = ClusteringService()
priority_service = PriorityService()
ai_service = AIService()

@router.post("/cluster")
async def cluster_feedbacks(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Cluster recent feedbacks into issues"""
    
    # Get recent feedbacks
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    feedbacks = db.query(Feedback).filter(
        Feedback.created_at >= cutoff_date
    ).all()
    
    if not feedbacks:
        return {"message": "No feedbacks to cluster"}
    
    # Convert to dict
    feedback_dicts = [
        {
            "id": f.id,
            "content": f.content,
            "title": f.title,
            "rating": f.rating,
            "sentiment": str(f.sentiment) if f.sentiment else None,
            "embedding": f.embedding,
            "platform": str(f.platform),
            "app_version": f.app_version,
            "region": f.region,
            "device_info": f.device_info
        }
        for f in feedbacks
    ]
    
    # Cluster
    clusters = clustering_service.cluster_feedbacks(feedback_dicts)
    
    total_feedbacks = len(feedbacks)
    created_issues = []
    
    # Process each cluster
    for cluster_id, cluster_feedbacks in clusters.items():
        if cluster_id == -1:  # Skip noise cluster
            continue
        
        if len(cluster_feedbacks) < 2:  # Skip single-item clusters
            continue
        
        # Extract keywords
        keywords = clustering_service.find_cluster_keywords(cluster_feedbacks)
        
        # Categorize
        sample_text = cluster_feedbacks[0]['content']
        category = await ai_service.categorize_issue(sample_text)
        
        # Generate title
        title = clustering_service.generate_cluster_title(keywords, category)
        
        # Calculate severity
        severity = clustering_service.calculate_cluster_severity(cluster_feedbacks)
        
        # Detect affected segments
        segments = clustering_service.detect_affected_segments(cluster_feedbacks)
        
        # Calculate metrics
        complaint_count = len(cluster_feedbacks)
        complaint_percentage = priority_service.calculate_complaint_percentage(
            complaint_count,
            total_feedbacks
        )
        
        # Create or update issue
        issue = Issue(
            title=title,
            category=category,
            severity=Severity(severity),
            complaint_count=complaint_count,
            complaint_percentage=complaint_percentage,
            affected_platforms=segments['platforms'],
            affected_versions=segments['versions'],
            affected_regions=segments['regions'],
            affected_devices=segments['devices'],
            cluster_id=cluster_id,
            keywords=keywords,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        
        # Calculate priority
        issue_dict = {
            'complaint_count': complaint_count,
            'severity': severity,
            'trend': 'stable',
            'affected_users': complaint_count,
            'last_seen': datetime.utcnow()
        }
        priority_score = priority_service.calculate_priority_score(issue_dict)
        issue.priority = Priority(
            priority_service.assign_priority(priority_score, severity)
        )
        
        db.add(issue)
        created_issues.append({
            "title": title,
            "severity": severity,
            "complaints": complaint_count,
            "percentage": complaint_percentage
        })
    
    db.commit()
    
    return {
        "message": f"Created {len(created_issues)} issues from {len(clusters)} clusters",
        "issues": created_issues
    }

@router.get("/priorities")
async def get_priorities(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get prioritized list of issues"""
    
    issues = db.query(Issue).filter(
        Issue.is_resolved == False
    ).all()
    
    # Convert to dict
    issue_dicts = [
        {
            "id": i.id,
            "title": i.title,
            "category": i.category,
            "severity": str(i.severity),
            "priority": str(i.priority),
            "trend": str(i.trend),
            "complaint_count": i.complaint_count,
            "complaint_percentage": i.complaint_percentage,
            "affected_users": i.affected_users,
            "affected_platforms": i.affected_platforms,
            "affected_versions": i.affected_versions,
            "keywords": i.keywords,
            "last_seen": i.last_seen
        }
        for i in issues
    ]
    
    # Rank by priority
    priorities = priority_service.get_top_priorities(issue_dicts, limit)
    
    return {
        "priorities": priorities,
        "total_issues": len(issues)
    }

@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard overview data"""
    
    # Total stats
    total_feedbacks = db.query(Feedback).count()
    total_issues = db.query(Issue).filter(Issue.is_resolved == False).count()
    
    # Top pain points (by complaint count)
    top_issues = db.query(Issue).filter(
        Issue.is_resolved == False
    ).order_by(desc(Issue.complaint_count)).limit(5).all()
    
    # Severity breakdown
    severity_breakdown = db.query(
        Issue.severity,
        func.count(Issue.id)
    ).filter(
        Issue.is_resolved == False
    ).group_by(Issue.severity).all()
    
    # Sentiment breakdown
    sentiment_breakdown = db.query(
        Feedback.sentiment,
        func.count(Feedback.id)
    ).group_by(Feedback.sentiment).all()
    
    # Trending issues (increasing trend)
    trending = db.query(Issue).filter(
        Issue.trend == Trend.INCREASING,
        Issue.is_resolved == False
    ).order_by(desc(Issue.complaint_percentage)).limit(5).all()
    
    return {
        "overview": {
            "total_feedbacks": total_feedbacks,
            "active_issues": total_issues,
            "critical_issues": db.query(Issue).filter(
                Issue.severity == Severity.CRITICAL,
                Issue.is_resolved == False
            ).count()
        },
        "top_pain_points": [
            {
                "title": i.title,
                "complaints": i.complaint_count,
                "percentage": i.complaint_percentage,
                "severity": str(i.severity),
                "trend": str(i.trend)
            }
            for i in top_issues
        ],
        "severity_breakdown": {
            str(s): c for s, c in severity_breakdown
        },
        "sentiment_breakdown": {
            str(s): c for s, c in sentiment_breakdown
        },
        "trending_issues": [
            {
                "title": i.title,
                "trend": str(i.trend),
                "change_percentage": i.complaint_percentage
            }
            for i in trending
        ]
    }

@router.get("/issue/{issue_id}")
async def get_issue_details(
    issue_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about an issue"""
    
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(404, "Issue not found")
    
    # Get suggested fix
    issue_dict = {
        "title": issue.title,
        "description": issue.description or issue.title,
        "category": issue.category,
        "severity": str(issue.severity),
        "affected_platforms": issue.affected_platforms,
        "affected_versions": issue.affected_versions,
        "affected_regions": issue.affected_regions
    }
    
    suggested_fix = await ai_service.suggest_fix(
        issue.title,
        {
            "platforms": issue.affected_platforms,
            "versions": issue.affected_versions,
            "regions": issue.affected_regions
        }
    )
    
    return {
        "issue": issue_dict,
        "metrics": {
            "complaint_count": issue.complaint_count,
            "complaint_percentage": issue.complaint_percentage,
            "affected_users": issue.affected_users,
            "trend": str(issue.trend)
        },
        "timeline": {
            "first_seen": issue.first_seen,
            "last_seen": issue.last_seen,
            "created_at": issue.created_at
        },
        "suggested_fix": suggested_fix,
        "should_create_ticket": priority_service.should_create_ticket(issue_dict)
    }