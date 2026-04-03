"""Database initialization script to create all tables."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import create_all_tables, Base, engine
from app.models.db_models import (
    User, UserProgress, ChatSession, Chat, Document,
    Topic, LearningPath, Recommendation, Quiz, QuizResult,
    Feedback, Analytics, Nudge, SkillLevel, LearningMode
)


def init_db():
    """Initialize database and create all tables."""
    try:
        print("Creating database tables...")
        create_all_tables()
        print("✅ Database successfully initialized!")
        print(f"Connected to database via SQLAlchemy")
        print(f"All tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
