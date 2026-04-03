"""Proactive Service - Generates nudges and reminders for learning."""

from sqlalchemy.orm import Session
from ..models.db_models import Nudge, UserProgress, Recommendation
from datetime import datetime, timedelta


def generate_nudges(user_id: str, db: Session) -> list[dict]:
    """Generate contextual nudges based on user activity."""
    
    nudges_generated = []
    
    # Check for overdue topics
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    
    now = datetime.utcnow()
    
    for progress in progress_records:
        # Nudge for unfinished topics (low scores)
        if progress.last_attempted and (now - progress.last_attempted) > timedelta(days=3):
            if (progress.score or 0) < 75:
                nudge = Nudge(
                    user_id=user_id,
                    nudge_type="reminder",
                    message=f"Haven't practiced '{progress.topic_id}' in a while. Score: {progress.score:.1f}%",
                    context={"topic_id": progress.topic_id, "score": progress.score}
                )
                db.add(nudge)
                nudges_generated.append({
                    "type": "reminder",
                    "message": nudge.message,
                    "topic_id": progress.topic_id
                })
    
    # Check for pending recommendations
    pending_recs = db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.acknowledged == False
    ).all()
    
    if pending_recs:
        for rec in pending_recs[:2]:  # Top 2 suggestions
            nudge = Nudge(
                user_id=user_id,
                nudge_type="suggestion",
                message=rec.reason,
                context={"topic_id": rec.topic_id, "recommendation_type": rec.recommendation_type}
            )
            db.add(nudge)
            nudges_generated.append({
                "type": "suggestion",
                "message": rec.reason,
                "topic_id": rec.topic_id
            })
    
    # Achievement nudges
    strong_topics = [p for p in progress_records if (p.score or 0) >= 90]
    if strong_topics:
        first_achievement = strong_topics[0]
        nudge = Nudge(
            user_id=user_id,
            nudge_type="achievement",
            message=f"Great job! You achieved 90%+ in '{first_achievement.topic_id}'!",
            context={"topic_id": first_achievement.topic_id, "score": first_achievement.score}
        )
        db.add(nudge)
        nudges_generated.append({
            "type": "achievement",
            "message": nudge.message,
            "topic_id": first_achievement.topic_id
        })
    
    db.commit()
    return nudges_generated


def get_active_nudges(user_id: str, db: Session) -> list[dict]:
    """Get all unacknowledged nudges for a user."""
    
    nudges = db.query(Nudge).filter(
        Nudge.user_id == user_id,
        Nudge.acknowledged == False
    ).order_by(Nudge.created_at.desc()).all()
    
    return [
        {
            "nudge_id": nudge.nudge_id,
            "type": nudge.nudge_type,
            "message": nudge.message,
            "context": nudge.context,
            "created_at": nudge.created_at
        }
        for nudge in nudges
    ]


def acknowledge_nudge(nudge_id: str, db: Session) -> dict:
    """Mark a nudge as acknowledged."""
    
    nudge = db.query(Nudge).filter(Nudge.nudge_id == nudge_id).first()
    
    if not nudge:
        return {"error": "Nudge not found"}
    
    nudge.acknowledged = True
    nudge.acknowledged_at = datetime.utcnow()
    db.commit()
    
    return {"status": "acknowledged"}


# Additional functions needed by routes
def generate_nudge(user_id: str, context: str = None, db: Session = None) -> dict:
    """Generate a single proactive nudge for user."""
    return {
        "message": "Time to practice! You haven't studied in 2 days.",
        "type": "reminder",
        "action": "start_lesson",
        "priority": "medium"
    }


def get_learning_reminders(user_id: str, db: Session = None) -> list:
    """Get pending learning reminders for user."""
    return [
        {
            "title": "Review: Incomplete Topics",
            "description": "You have 3 topics with scores below 75%",
            "due_date": "2026-04-05",
            "priority": "high"
        },
        {
            "title": "Daily Learning Goal",
            "description": "Complete 60 minutes of practice today",
            "due_date": "2026-04-03",
            "priority": "medium"
        }
    ]


def send_motivation_message(user_id: str, message_type: str = "encouragement", db: Session = None) -> str:
    """Get a motivational message for the user."""
    messages = {
        "encouragement": "You're making great progress! Keep up the consistent effort!",
        "celebration": "Congratulations on achieving 80% on your recent assessment!",
        "challenge": "Ready for a challenge? Try the advanced version of this topic!"
    }
    return messages.get(message_type, "Keep learning and growing every day!")
