"""Proactive support and AI-driven notifications endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..services.proactive_service import (
    generate_nudge,
    get_learning_reminders,
    send_motivation_message
)

router = APIRouter(prefix="/proactive", tags=["Proactive Support"])


class NudgeResponse(BaseModel):
    """Proactive nudge response."""
    message: str
    type: str
    action: str
    priority: str


@router.get("/nudge")
async def get_proactive_nudge(
    user_id: str = "demo-user",
    context: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get proactive learning nudges and reminders.
    
    Returns personalized suggestions to keep user engaged with learning.
    """
    try:
        nudge = generate_nudge(user_id, context, db)
        return {
            "status": "success",
            "nudge": nudge
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reminders")
async def get_learning_reminders(
    user_id: str = "demo-user",
    db: Session = Depends(get_db)
):
    """
    Get pending learning reminders for the user.
    
    Returns list of tasks and deadlines that need attention.
    """
    try:
        reminders = get_learning_reminders(user_id, db)
        return {
            "status": "success",
            "reminders": reminders,
            "total_pending": len(reminders)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/motivation")
async def get_motivation_message(
    user_id: str = "demo-user",
    message_type: str = "encouragement",
    db: Session = Depends(get_db)
):
    """
    Get personalized motivation messages to encourage learning.
    
    - **message_type**: Type of motivation (encouragement, celebration, challenge)
    
    Returns an AI-generated motivational message personalized to user's progress.
    """
    try:
        message = send_motivation_message(user_id, message_type, db)
        return {
            "status": "success",
            "message": message,
            "type": message_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
