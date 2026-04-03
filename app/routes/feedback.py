"""AI-driven feedback endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.feedback_service import (
    generate_feedback,
    get_recent_feedback
)

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/{user_id}/{topic_id}")
async def generate_feedback_endpoint(user_id: str, topic_id: str, db: Session = Depends(get_db)):
    """Generate AI feedback for user performance."""
    try:
        feedback = await generate_feedback(user_id, topic_id, db)
        return {"status": "success", "data": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}")
async def get_feedback(user_id: str, limit: int = 5, db: Session = Depends(get_db)):
    """Get recent feedback for user."""
    try:
        feedbacks = get_recent_feedback(user_id, db, limit)
        return {"status": "success", "data": feedbacks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
