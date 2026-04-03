"""Session management routes."""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models.session_models import SessionCreateResponse, SessionInfo
from app.services.session_service import session_service
from app.core.config import settings

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/create", response_model=SessionCreateResponse)
async def create_session() -> SessionCreateResponse:
    """Create a new chat session (no user_id needed - uses session-based auth)."""
    try:
        session_id = session_service.create_session()
        session_info = session_service.get_session_info(session_id)
        
        return SessionCreateResponse(
            session_id=session_id,
            created_at=session_info["created_at"],
            status="active"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

