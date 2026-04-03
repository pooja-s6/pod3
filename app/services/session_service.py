"""Session Service for managing user sessions."""

import uuid
from datetime import datetime
from app.utils.memory import session_memory
from typing import Dict, List, Optional


class SessionService:
    """Service for managing chat sessions."""
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new session for a user. user_id is optional for session-based auth."""
        session_id = str(uuid.uuid4())
        session_memory.create_session(session_id, user_id)
        return session_id
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get information about a session."""
        return session_memory.get_session_info(session_id)
    
    def add_message_to_session(self, session_id: str, role: str, content: str) -> None:
        """Add a message to session history."""
        session_memory.add_message(session_id, role, content)
    
    def get_session_context(self, session_id: str, max_messages: int = 5) -> List[Dict]:
        """Get conversation context (last N messages) for a session."""
        return session_memory.get_context(session_id, max_messages)
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get all messages in a session."""
        return session_memory.get_all_messages(session_id)
    
    def get_user_sessions(self, user_id: str) -> List[str]:
        """Get all session IDs for a user."""
        return session_memory.get_user_sessions(user_id)
    
    def validate_session(self, session_id: str) -> bool:
        """Check if session exists and is valid."""
        return session_id in session_memory.sessions
    
    def get_session_message_count(self, session_id: str) -> int:
        """Get total message count in a session."""
        if session_id not in session_memory.sessions:
            return 0
        return session_memory.sessions[session_id]["message_count"]
    
    def cleanup_expired_sessions(self, timeout_seconds: int = 3600) -> None:
        """Remove expired sessions."""
        session_memory.clear_expired_sessions(timeout_seconds)


# Global session service instance
session_service = SessionService()
