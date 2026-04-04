"""Chat routes for AI interactions."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import uuid
import time
from datetime import datetime

from ..models.chat_models import ChatRequest, ChatResponse, StreamChatRequest, ChatHistory
from ..services.core import ai_service, prompt_builder, rag_service
from ..services.chatbot import session_service, analytics_service
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


@router.post("/quick-suggestions")
async def get_quick_suggestions(
    session_id: str,
    concept: str,
    topic_id: str = None
) -> dict:
    """
    Get quick suggestion prompts for expandable chat pop-up.
    
    Perfect for non-intrusive contextual AI support during lessons or quizzes.
    Returns 3-4 quick suggestion prompts like:
    - "Explain this concept"
    - "Give an example"
    - "Simplify this"
    - "How does this relate to..."
    
    Args:
        session_id: Current session ID
        concept: The concept or text to get suggestions for
        topic_id: Optional topic ID for contextual suggestions
        
    Returns:
        List of quick suggestion prompts and their descriptions
    """
    try:
        # Validate session
        if not session_service.validate_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Build contextual prompts
        system_prompt = f"""You are a helpful learning assistant providing quick suggestion prompts.
        
Given the concept: "{concept}"
{"and topic: " + topic_id if topic_id else ""}

Generate exactly 4 quick, helpful suggestion prompts that a student might click on.
Each should be concise (under 10 words) and action-oriented.

Format as JSON array with this structure:
[
  {{"text": "Suggestion text", "description": "What this will do"}},
  ...
]"""
        
        suggestions_json = ai_service.chat(
            system_prompt=system_prompt,
            messages=[],
            user_message="Generate quick suggestions"
        )
        
        # Parse suggestions (basic parsing, assume AI returns valid JSON)
        try:
            import json
            suggestions = json.loads(suggestions_json)
        except:
            # Fallback suggestions if parsing fails
            suggestions = [
                {"text": "Explain this", "description": "Get a detailed explanation"},
                {"text": "Give examples", "description": "See practical examples"},
                {"text": "Simplify", "description": "Make it easier to understand"},
                {"text": "Key points", "description": "Focus on main ideas"}
            ]
        
        return {
            "status": "success",
            "session_id": session_id,
            "concept": concept,
            "quick_suggestions": suggestions,
            "timestamp": datetime.now()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/contextual")
async def contextual_chat(
    session_id: str,
    message: str,
    lesson_id: str = None,
    quiz_id: str = None,
    context_type: str = "lesson"
):
    """
    Contextual AI support during lessons or quizzes.
    
    Provides intelligent assistance without disrupting the learning flow.
    Perfect for embedding in lesson/quiz UI as non-intrusive expandable chat.
    
    Args:
        session_id: Current session/student ID
        message: Student's question or request
        lesson_id: Current lesson ID (if in lesson)
        quiz_id: Current quiz ID (if taking quiz)
        context_type: "lesson" or "quiz"
        
    Returns:
        AI response contextual to current activity
    """
    try:
        # Validate session
        if not session_service.validate_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Build contextual system prompt
        if context_type == "quiz":
            system_prompt = f"""You are a helpful learning assistant supporting a student during a quiz.
            
Quiz ID: {quiz_id}

IMPORTANT GUIDELINES:
- Provide hints but NOT direct answers
- Help clarify the question if student is confused
- Suggest thinking approaches
- Don't give away the answer
- Be encouraging and supportive"""
        else:  # lesson
            system_prompt = f"""You are a patient learning assistant helping during a lesson.
            
Lesson ID: {lesson_id}

GUIDELINES:
- Explain concepts clearly
- Provide examples when helpful
- Check understanding with questions
- Break down complex ideas
- Be encouraging"""
        
        # Get conversation context
        context_messages = session_service.get_session_context(
            session_id,
            max_messages=3  # Shorter context for quick pop-up
        )
        
        # Get AI response
        ai_response = ai_service.chat(
            system_prompt=system_prompt,
            messages=context_messages,
            user_message=message
        )
        
        # Store in session
        session_service.add_message_to_session(session_id, "user", message)
        session_service.add_message_to_session(session_id, "assistant", ai_response)
        
        # Log to analytics
        query_id = str(uuid.uuid4())
        analytics_service.log_query(
            query_id=query_id,
            session_id=session_id,
            message=message,
            mode="contextual_help",
            response_time=0
        )
        
        return {
            "status": "success",
            "session_id": session_id,
            "response": ai_response,
            "context_type": context_type,
            "context_id": lesson_id or quiz_id,
            "timestamp": datetime.now(),
            "non_intrusive": True
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
