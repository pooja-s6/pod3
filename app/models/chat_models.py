from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    session_id: str
    message: str
    mode: Literal["teaching", "guiding", "normal"] = "normal"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    session_id: str
    user_message: str
    ai_response: str
    mode: str
    timestamp: datetime


class StreamChatRequest(BaseModel):
    """Request model for streaming chat endpoint."""
    session_id: str
    message: str
    mode: Literal["teaching", "guiding", "normal"] = "normal"


class Message(BaseModel):
    """Individual message in conversation."""
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime


class ChatHistory(BaseModel):
    """Chat history response."""
    session_id: str
    messages: list[Message]
    total_messages: int
