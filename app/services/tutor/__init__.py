"""Tutor Services - Adaptive learning, progress tracking, and recommendations."""

from .adaptive_service import get_adaptive_learning_path, get_difficulty_adjustment, create_personalized_quiz
from .learning_path_service import generate_learning_path
from .progress_service import update_user_progress, batch_update_progress, get_user_statistics
from .feedback_service import evaluate_answer, generate_feedback, get_recent_feedback
from .recommendation_service import generate_recommendations, get_recommendations, acknowledge_recommendation
from .summary_service import generate_study_summary
from .proactive_service import check_user_engagement, send_proactive_message, generate_nudges, get_active_nudges, acknowledge_nudge

__all__ = [
    "get_adaptive_learning_path",
    "get_difficulty_adjustment",
    "create_personalized_quiz",
    "generate_learning_path",
    "update_user_progress",
    "batch_update_progress",
    "get_user_statistics",
    "evaluate_answer",
    "generate_feedback",
    "get_recent_feedback",
    "generate_recommendations",
    "get_recommendations",
    "acknowledge_recommendation",
    "generate_study_summary",
    "check_user_engagement",
    "send_proactive_message",
    "generate_nudges",
    "get_active_nudges",
    "acknowledge_nudge"
]
