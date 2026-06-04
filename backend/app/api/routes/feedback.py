from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import io
from datetime import datetime

from app.models.database import get_db
from app.models.feedback import Feedback, Platform, Sentiment
from app.services.ai_service import AIService
from pydantic import BaseModel

router = APIRouter()
ai_service = AIService()

class FeedbackCreate(BaseModel):
    platform: str
    content: str
    title: Optional[str] = None
    rating: Optional[float] = None
    user_id: Optional[str] = None
    app_version: Optional[str] = None
    region: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    platform: str
    content: str
    sentiment: Optional[str]
    rating: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process CSV of feedbacks"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "File must be CSV")
    
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Validate required columns
        required_cols = ['content']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(400, f"CSV must contain: {required_cols}")
        
        # Process each row
        processed = 0
        for _, row in df.iterrows():
            # Create feedback
            feedback = Feedback(
                platform=Platform.CSV,
                content=row.get('content', ''),
                title=row.get('title'),
                rating=row.get('rating'),
                user_id=row.get('user_id'),
                app_version=row.get('app_version'),
                region=row.get('region'),
                feedback_date=datetime.utcnow()
            )
            
            # AI Analysis
            sentiment_result = await ai_service.analyze_sentiment(feedback.content)
            feedback.sentiment = Sentiment(sentiment_result['sentiment'])
            feedback.sentiment_score = sentiment_result['score']
            
            # Generate embedding
            embedding = await ai_service.get_embedding(feedback.content)
            feedback.embedding = embedding
            
            feedback.processed_at = datetime.utcnow()
            
            db.add(feedback)
            processed += 1
        
        db.commit()
        
        return {
            "message": f"Processed {processed} feedbacks",
            "count": processed
        }
    
    except Exception as e:
        raise HTTPException(500, f"Error processing CSV: {str(e)}")

@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Create a single feedback entry"""
    
    # Create feedback
    feedback = Feedback(
        platform=Platform(feedback_data.platform),
        content=feedback_data.content,
        title=feedback_data.title,
        rating=feedback_data.rating,
        user_id=feedback_data.user_id,
        app_version=feedback_data.app_version,
        region=feedback_data.region,
        feedback_date=datetime.utcnow()
    )
    
    # AI Analysis
    sentiment_result = await ai_service.analyze_sentiment(feedback.content)
    feedback.sentiment = Sentiment(sentiment_result['sentiment'])
    feedback.sentiment_score = sentiment_result['score']
    
    # Generate embedding
    embedding = await ai_service.get_embedding(feedback.content)
    feedback.embedding = embedding
    
    feedback.processed_at = datetime.utcnow()
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback

@router.get("/", response_model=List[FeedbackResponse])
async def list_feedbacks(
    skip: int = 0,
    limit: int = 100,
    platform: Optional[str] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List feedbacks with filters"""
    query = db.query(Feedback)
    
    if platform:
        query = query.filter(Feedback.platform == Platform(platform))
    
    if sentiment:
        query = query.filter(Feedback.sentiment == Sentiment(sentiment))
    
    feedbacks = query.offset(skip).limit(limit).all()
    return feedbacks

@router.get("/stats")
async def get_feedback_stats(db: Session = Depends(get_db)):
    """Get feedback statistics"""
    total = db.query(Feedback).count()
    
    by_platform = db.query(
        Feedback.platform,
        db.func.count(Feedback.id)
    ).group_by(Feedback.platform).all()
    
    by_sentiment = db.query(
        Feedback.sentiment,
        db.func.count(Feedback.id)
    ).group_by(Feedback.sentiment).all()
    
    return {
        "total_feedbacks": total,
        "by_platform": {str(p): c for p, c in by_platform},
        "by_sentiment": {str(s): c for s, c in by_sentiment}
    }