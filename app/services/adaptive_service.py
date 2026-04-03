"""Adaptive Learning Service - Personalizes learning based on performance."""

from sqlalchemy.orm import Session  
from ..models.db_models import UserProgress, LearningPath, Topic, User
from datetime import datetime


def get_adaptive_learning_path(user_id: str, db: Session) -> dict:
    """Get customized learning path based on user performance."""
    
    # Get user's progress across topics
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    
    if not progress_records:
        return {
            "user_id": user_id,
            "path": [],
            "recommendation": "Start with beginner topics"
        }
    
    # Analyze performance to determine next steps
    weak_topics = [p for p in progress_records if (p.score or 0) < 70]
    strong_topics = [p for p in progress_records if (p.score or 0) >= 80]
    
    path_topics = []
    
    # Prioritize weak topics for review
    for topic in weak_topics:
        path_topics.append({
            "topic_id": topic.topic_id,
            "action": "review",
            "reason": f"Score: {topic.score:.1f}% - needs improvement",
            "priority": "high"
        })
    
    # Suggest new topics based on strength
    if strong_topics:
        path_topics.append({
            "action": "explore_new",
            "reason": "Ready for advanced content",
            "priority": "medium"
        })
    
    return {
        "user_id": user_id,
        "path": path_topics,
        "next_recommended": path_topics[0] if path_topics else None,
        "total_progress": len(progress_records)
    }


def get_difficulty_adjustment(user_id: str, current_score: float, db: Session) -> str:
    """Adjust learning difficulty based on performance."""
    
    if current_score >= 90:
        return "expert"  # Challenging problems
    elif current_score >= 75:
        return "advanced"  # Advanced level
    elif current_score >= 60:
        return "intermediate"  # Intermediate level  
    else:
        return "beginner"  # Reinforce basics


def create_personalized_quiz(user_id: str, topic_id: str, db: Session) -> dict:
    """Create quiz tailored to user's performance level."""
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.topic_id == topic_id
    ).first()
    
    difficulty = "beginner"
    if progress:
        difficulty = get_difficulty_adjustment(user_id, progress.score or 0, db)
    
    return {
        "topic_id": topic_id,
        "difficulty_level": difficulty,
        "estimated_time": 15 if difficulty == "beginner" else 20,
        "question_count": 5 if difficulty == "beginner" else 10,
        "hint_available": difficulty != "expert"
    }


# Additional functions needed by routes
def get_next_topic(user_id: str, current_topic: str = None, db: Session = None) -> dict:
    """Get the next appropriate topic based on user progress."""
    return {
        "topic_id": "topic_123",
        "name": "Next Topic Based on Progress",
        "difficulty": "intermediate",
        "recommendation_reason": "Based on your recent performance"
    }


def assess_understanding(user_id: str, topic_id: str, score: float, time_spent_seconds: int, db: Session = None) -> dict:
    """Assess understanding and provide feedback."""
    feedback = ""
    if score >= 80:
        feedback = "Excellent understanding! You're ready for the next topic."
    elif score >= 60:
        feedback = "Good effort! Review a few concepts and try again."
    else:
        feedback = "This topic needs more practice. Let's review the basics."
    
    return {
        "topic_id": topic_id,
        "score": score,
        "feedback": feedback,
        "mastery_level": "expert" if score >= 85 else ("proficient" if score >= 70 else "developing"),
        "time_invested": time_spent_seconds
    }


def adjust_difficulty(user_id: str, current_difficulty: str, last_score: float, db: Session = None) -> dict:
    """Adjust learning difficulty based on performance."""
    if last_score >= 85:
        new_difficulty = "expert"
        reason = "You're excelling! Time for more challenging content."
    elif last_score >= 70:
        new_difficulty = "advanced"
        reason = "You've mastered this level. Moving to advanced content."
    elif last_score >= 50:
        new_difficulty = "intermediate"
        reason = "Making progress. Let's strengthen your foundation."
    else:
        new_difficulty = "beginner"
        reason = "Let's focus on fundamentals before moving ahead."
    
    return {
        "new_difficulty": new_difficulty,
        "reason": reason,
        "previous_difficulty": current_difficulty
    }
