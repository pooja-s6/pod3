"""Progress Tracking Service - Manages user learning progress."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.db_models import UserProgress, User, SkillLevel
from datetime import datetime


def update_user_progress(user_id: str, topic_id: str, is_correct: bool, db: Session) -> dict:
    """Update user progress after a quiz attempt."""
    
    # Fetch or create progress record
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            topic_id=topic_id,
            score=0.0,
            attempts=0,
            correct_answers=0,
            total_questions=0
        )
        db.add(progress)
    
    # Update attempt counters
    progress.attempts = (progress.attempts or 0) + 1
    progress.total_questions = (progress.total_questions or 0) + 1
    
    if is_correct:
        progress.correct_answers = (progress.correct_answers or 0) + 1
    
    # Calculate score percentage
    progress.score = (progress.correct_answers / progress.total_questions) * 100
    progress.last_attempted = datetime.utcnow()
    progress.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    
    return {
        "progress_id": progress.progress_id,
        "topic_id": progress.topic_id,
        "score": round(progress.score, 2),
        "attempts": progress.attempts,
        "correct_answers": progress.correct_answers,
        "total_questions": progress.total_questions
    }


def batch_update_progress(user_id: str, topic_id: str, correct: int, total: int, db: Session) -> dict:
    """Batch update progress for multiple questions."""
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            topic_id=topic_id,
            score=0.0,
            attempts=0,
            correct_answers=0,
            total_questions=0
        )
        db.add(progress)
    
    progress.attempts = (progress.attempts or 0) + 1
    progress.correct_answers = (progress.correct_answers or 0) + correct
    progress.total_questions = (progress.total_questions or 0) + total
    progress.score = (progress.correct_answers / progress.total_questions) * 100
    progress.last_attempted = datetime.utcnow()
    progress.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    
    return {
        "progress_id": progress.progress_id,
        "topic_id": progress.topic_id,
        "score": round(progress.score, 2),
        "attempts": progress.attempts,
        "correct_answers": progress.correct_answers,
        "total_questions": progress.total_questions
    }


def get_user_statistics(user_id: str, db: Session) -> dict:
    """Get overall user learning statistics."""
    
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    
    if not progress_records:
        return {
            "user_id": user_id,
            "total_topics": 0,
            "average_score": 0.0,
            "total_attempts": 0,
            "total_time_spent": 0
        }
    
    total_score = sum(p.score or 0 for p in progress_records)
    total_attempts = sum(p.attempts or 0 for p in progress_records)
    total_time = sum(p.time_spent or 0 for p in progress_records)
    
    return {
        "user_id": user_id,
        "total_topics": len(progress_records),
        "average_score": round(total_score / len(progress_records), 2),
        "total_attempts": total_attempts,
        "total_time_spent_seconds": total_time,
        "topics": [
            {
                "topic_id": p.topic_id,
                "score": round(p.score or 0, 2),
                "attempts": p.attempts
            }
            for p in progress_records
        ]
    }


def get_topic_progress(user_id: str, topic_id: str, db: Session) -> dict:
    """Get specific topic progress for a user."""
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id
    ).first()
    
    if not progress:
        return {"status": "not_started"}
    
    return {
        "progress_id": progress.progress_id,
        "topic_id": progress.topic_id,
        "score": round(progress.score or 0, 2),
        "attempts": progress.attempts or 0,
        "correct_answers": progress.correct_answers or 0,
        "total_questions": progress.total_questions or 0,
        "time_spent_seconds": progress.time_spent or 0,
        "last_attempted": progress.last_attempted
    }
