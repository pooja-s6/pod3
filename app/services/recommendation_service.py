"""Recommendation Service - Personalized learning recommendations."""

from sqlalchemy.orm import Session
from ..models.db_models import Recommendation, UserProgress, Topic, User
from datetime import datetime


async def generate_recommendations(user_id: str, db: Session) -> list[dict]:
    """Generate personalized learning recommendations based on performance."""
    
    # Get user's progress
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    
    recommendations = []
    
    # Analyze performance and create recommendations
    for progress in progress_records:
        if progress.score and progress.score < 60:
            # Recommend review for low scores
            rec = Recommendation(
                user_id=user_id,
                topic_id=progress.topic_id,
                recommendation_type="review",
                reason=f"Your score in this topic is {progress.score:.1f}%. Consider reviewing the material.",
                confidence_score=0.9
            )
            db.add(rec)
        elif progress.score and progress.score >= 80:
            # Recommend new topic for strong performance
            rec = Recommendation(
                user_id=user_id,
                topic_id=progress.topic_id,
                recommendation_type="new_topic",
                reason="You're doing well! Ready for a new topic?",
                confidence_score=0.85
            )
            db.add(rec)
        else:
            # Recommend practice for average performance
            rec = Recommendation(
                user_id=user_id,
                topic_id=progress.topic_id,
                recommendation_type="practice",
                reason="Keep practicing to improve your understanding.",
                confidence_score=0.8
            )
            db.add(rec)
    
    db.commit()
    
    # Return active recommendations
    active_recs = db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.acknowledged == False
    ).all()
    
    return [
        {
            "recommendation_id": rec.recommendation_id,
            "topic_id": rec.topic_id,
            "type": rec.recommendation_type,
            "reason": rec.reason,
            "confidence": rec.confidence_score
        }
        for rec in active_recs
    ]


def get_recommendations(user_id: str, db: Session) -> list[dict]:
    """Get active recommendations for a user."""
    
    recs = db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.acknowledged == False
    ).all()
    
    return [
        {
            "recommendation_id": rec.recommendation_id,
            "topic_id": rec.topic_id,
            "type": rec.recommendation_type,
            "reason": rec.reason,
            "confidence": rec.confidence_score,
            "created_at": rec.created_at
        }
        for rec in recs
    ]


def acknowledge_recommendation(recommendation_id: str, db: Session) -> dict:
    """Mark recommendation as acknowledged."""
    
    rec = db.query(Recommendation).filter(
        Recommendation.recommendation_id == recommendation_id
    ).first()
    
    if not rec:
        return {"error": "Recommendation not found"}
    
    rec.acknowledged = True
    db.commit()
    db.refresh(rec)
    
    return {"status": "acknowledged"}
