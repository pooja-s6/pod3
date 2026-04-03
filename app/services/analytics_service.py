"""Analytics Service for tracking usage and insights."""

from datetime import datetime
from typing import Dict, List, Optional
import json


class AnalyticsService:
    """Service for tracking and analyzing user interactions."""
    
    def __init__(self):
        self.query_logs: List[Dict] = []
        self.user_stats: Dict = {}
        self.session_stats: Dict = {}
    
    def log_query(self, query_id: str, session_id: str, message: str, 
                  mode: str, response_time: float, user_id: Optional[str] = None) -> None:
        """Log a user query."""
        log_entry = {
            "query_id": query_id,
            "session_id": session_id,
            "user_id": user_id,
            "message": message,
            "mode": mode,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.query_logs.append(log_entry)
        
        # Only update user stats if user_id is provided
        if user_id:
            # Update user stats
            if user_id not in self.user_stats:
                self.user_stats[user_id] = {
                    "total_queries": 0,
                    "mode_usage": {},
                    "total_response_time": 0.0,
                    "topics": []
                }
            
            self.user_stats[user_id]["total_queries"] += 1
            
            # Track mode usage
            if mode not in self.user_stats[user_id]["mode_usage"]:
                self.user_stats[user_id]["mode_usage"][mode] = 0
            self.user_stats[user_id]["mode_usage"][mode] += 1
            
            # Track response time
            self.user_stats[user_id]["total_response_time"] += response_time
    
    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user."""
        if user_id not in self.user_stats:
            return {
                "user_id": user_id,
                "total_queries": 0,
                "mode_usage": {},
                "avg_response_time": 0.0,
                "topics_discussed": []
            }
        
        stats = self.user_stats[user_id]
        avg_response_time = (
            stats["total_response_time"] / stats["total_queries"]
            if stats["total_queries"] > 0 else 0.0
        )
        
        return {
            "user_id": user_id,
            "total_queries": stats["total_queries"],
            "mode_usage": stats["mode_usage"],
            "avg_response_time": round(avg_response_time, 2),
            "topics_discussed": stats["topics"]
        }
    
    def get_session_analytics(self, session_id: str) -> Dict:
        """Get analytics for a specific session."""
        session_queries = [
            log for log in self.query_logs
            if log["session_id"] == session_id
        ]
        
        if not session_queries:
            return {
                "session_id": session_id,
                "total_queries": 0,
                "mode_usage": {},
                "avg_response_time": 0.0
            }
        
        mode_usage = {}
        total_response_time = 0.0
        
        for query in session_queries:
            mode = query["mode"]
            if mode not in mode_usage:
                mode_usage[mode] = 0
            mode_usage[mode] += 1
            total_response_time += query["response_time"]
        
        avg_response_time = total_response_time / len(session_queries)
        
        return {
            "session_id": session_id,
            "total_queries": len(session_queries),
            "mode_usage": mode_usage,
            "avg_response_time": round(avg_response_time, 2)
        }
    
    def get_global_analytics(self) -> Dict:
        """Get global platform analytics."""
        if not self.query_logs:
            return {
                "total_queries": 0,
                "total_users": 0,
                "total_sessions": 0,
                "mode_usage": {},
                "avg_response_time": 0.0
            }
        
        mode_usage = {}
        total_response_time = 0.0
        sessions = set()
        
        for query in self.query_logs:
            mode = query["mode"]
            if mode not in mode_usage:
                mode_usage[mode] = 0
            mode_usage[mode] += 1
            total_response_time += query["response_time"]
            sessions.add(query["session_id"])
        
        avg_response_time = total_response_time / len(self.query_logs)
        
        return {
            "total_queries": len(self.query_logs),
            "total_users": len(self.user_stats),
            "total_sessions": len(sessions),
            "mode_usage": mode_usage,
            "avg_response_time": round(avg_response_time, 2)
        }
    
    def extract_topics(self, text: str) -> List[str]:
        """Simple keyword extraction (can be enhanced with NLP)."""
        # This is a basic implementation
        # In production, use NLP libraries like SpaCy or NLTK
        stop_words = {"the", "a", "an", "is", "are", "what", "how", "when", "where", "why"}
        words = text.lower().split()
        topics = [
            word for word in words
            if len(word) > 3 and word not in stop_words
        ]
        return list(set(topics))[:5]  # Return top 5 unique topics


# Global analytics service instance
analytics_service = AnalyticsService()
