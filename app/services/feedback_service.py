"""Feedback Service - AI-driven feedback on learning performance."""

from sqlalchemy.orm import Session
from ..models.db_models import Feedback, UserProgress, Topic
from .ai_service import ai_service
from datetime import datetime


async def generate_feedback(user_id: str, topic_id: str, db: Session) -> dict:
    """Generate AI feedback based on user performance."""
    
    # Get progress record
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id
    ).first()
    
    if not progress:
        return {"error": "No progress found"}
    
    # Analyze performance and generate feedback
    score = progress.score or 0
    attempts = progress.attempts or 0
    
    if score < 50:
        feedback_type = "learning_gap"
        severity = "critical"
        prompt = f"User has low score ({score}%) in topic. Suggest specific areas to improve."
    elif score < 75:
        feedback_type = "performance"
        severity = "warning"
        prompt = f"User achieved {score}% in topic. Offer constructive feedback."
    else:
        feedback_type = "strength"
        severity = "info"
        prompt = f"User achieved {score}% in topic. Encourage to continue."
    
    # Generate AI feedback
    content = ai_service.chat(
        system_prompt="You are an educational coach providing feedback.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Save feedback
    feedback = Feedback(
        user_id=user_id,
        topic_id=topic_id,
        feedback_type=feedback_type,
        content=content,
        severity=severity
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return {
        "feedback_id": feedback.feedback_id,
        "type": feedback.feedback_type,
        "content": feedback.content,
        "severity": feedback.severity
    }


def get_recent_feedback(user_id: str, db: Session, limit: int = 5) -> list[dict]:
    """Get recent feedback for a user."""
    
    feedbacks = db.query(Feedback).filter(
        Feedback.user_id == user_id
    ).order_by(Feedback.created_at.desc()).limit(limit).all()
    
    return [
        {
            "feedback_id": fb.feedback_id,
            "topic_id": fb.topic_id,
            "type": fb.feedback_type,
            "content": fb.content,
            "severity": fb.severity,
            "created_at": fb.created_at
        }
        for fb in feedbacks
    ]
