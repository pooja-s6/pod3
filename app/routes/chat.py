"""Chat routes for AI interactions."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import uuid
import time
from datetime import datetime

from ..models.chat_models import ChatRequest, ChatResponse, StreamChatRequest, ChatHistory
from ..services.ai_service import ai_service
from ..services.session_service import session_service
from ..services.analytics_service import analytics_service
from ..services.prompt_builder import prompt_builder
from ..services.rag_service import rag_service
from ..core.config import settings

router = APIRouter(prefix="/ai", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for non-streaming responses.
    
    Supports three modes:
    - normal: Standard Q&A
    - teaching: Detailed explanations
    - guiding: Socratic method hints
    """
    try:
        # Validate session
        if not session_service.validate_session(request.session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Build system prompt
        system_prompt = prompt_builder.build_system_prompt(
            mode=request.mode
        )
        
        # Get conversation context
        context_messages = session_service.get_session_context(
            request.session_id,
            max_messages=settings.MAX_CONTEXT_MESSAGES
        )
        
        # Get AI response
        start_time = time.time()
        ai_response = ai_service.chat(
            system_prompt=system_prompt,
            messages=context_messages,
            user_message=request.message
        )
        response_time = time.time() - start_time
        
        # Store messages in session
        session_service.add_message_to_session(
            request.session_id, "user", request.message
        )
        session_service.add_message_to_session(
            request.session_id, "assistant", ai_response
        )
        
        # Log analytics
        query_id = str(uuid.uuid4())
        analytics_service.log_query(
            query_id=query_id,
            session_id=request.session_id,
            message=request.message,
            mode=request.mode,
            response_time=response_time
        )
        
        return ChatResponse(
            session_id=request.session_id,
            user_message=request.message,
            ai_response=ai_response,
            mode=request.mode,
            timestamp=datetime.now()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.get("/chat/history/{session_id}", response_model=ChatHistory)
async def get_chat_history(session_id: str) -> ChatHistory:
    """Get complete chat history for a session."""
    try:
        # Validate session
        if not session_service.validate_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        
        messages = session_service.get_session_history(session_id)
        session_info = session_service.get_session_info(session_id)
        
        # Convert to ChatHistory format
        formatted_messages = [
            {
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": datetime.fromisoformat(msg["timestamp"])
            }
            for msg in messages
        ]
        
        return ChatHistory(
            session_id=session_id,
            messages=formatted_messages,
            total_messages=len(messages)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
