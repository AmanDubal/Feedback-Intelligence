from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class Platform(str, enum.Enum):
    PLAYSTORE = "playstore"
    APPSTORE = "appstore"
    SUPPORT = "support"
    DISCORD = "discord"
    REDDIT = "reddit"
    CSV = "csv"

class Sentiment(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    platform = Column(Enum(Platform), nullable=False)
    
    # Content
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    rating = Column(Float, nullable=True)
    
    # Metadata
    user_id = Column(String, nullable=True)
    app_version = Column(String, nullable=True)
    device_info = Column(JSON, nullable=True)
    region = Column(String, nullable=True)
    
    # AI Analysis
    sentiment = Column(Enum(Sentiment), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    embedding = Column(JSON, nullable=True)  # Vector embedding
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    feedback_date = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    issues = relationship("FeedbackIssue", back_populates="feedback")

class FeedbackIssue(Base):
    __tablename__ = "feedback_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedbacks.id"))
    issue_id = Column(Integer, ForeignKey("issues.id"))
    confidence = Column(Float, default=0.0)
    
    feedback = relationship("Feedback", back_populates="issues")
    issue = relationship("Issue", back_populates="feedbacks")