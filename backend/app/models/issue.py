from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class Severity(str, enum.Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"

class Trend(str, enum.Enum):
    INCREASING = "increasing"
    STABLE = "stable"
    DECREASING = "decreasing"
    RESOLVED = "resolved"

class Priority(str, enum.Enum):
    IMMEDIATE = "immediate"
    NEXT_SPRINT = "next_sprint"
    LOW = "low"

class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Issue Details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    
    # Classification
    severity = Column(Enum(Severity), nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    trend = Column(Enum(Trend), default=Trend.STABLE)
    
    # Metrics
    complaint_count = Column(Integer, default=0)
    complaint_percentage = Column(Float, default=0.0)
    affected_users = Column(Integer, default=0)
    
    # Affected Segments
    affected_platforms = Column(JSON, nullable=True)  # ["android", "ios"]
    affected_versions = Column(JSON, nullable=True)   # ["4.2.1", "4.2.2"]
    affected_regions = Column(JSON, nullable=True)    # ["india", "us"]
    affected_devices = Column(JSON, nullable=True)    # ["iphone_12", "low_ram"]
    
    # AI Clustering
    cluster_id = Column(Integer, nullable=True)
    embedding = Column(JSON, nullable=True)
    keywords = Column(JSON, nullable=True)  # ["login", "otp", "verification"]
    
    # Integration
    jira_ticket_id = Column(String, nullable=True)
    github_issue_id = Column(String, nullable=True)
    
    # Status
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    feedbacks = relationship("FeedbackIssue", back_populates="issue")