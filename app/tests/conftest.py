import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.main import app
from app.core.database import Base, get_db
from app.models.db_models import (
    User, Session as SessionModel, ChatMessage, Progress, 
    Feedback, Recommendation, Document, Topic, Quiz, QuizResponse
)


# Create test database
@pytest.fixture(scope="session")
def test_db():
    """Create a test database"""
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Create a new database session for each test"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    connection = test_db.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with test database"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        user_id="test_user_123",
        email="test@example.com",
        name="Test User",
        learning_style="visual"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_session(db_session, test_user):
    """Create a test session"""
    session_obj = SessionModel(
        user_id=test_user.user_id,
        topic="Python Basics",
        session_start="2026-04-03T12:00:00"
    )
    db_session.add(session_obj)
    db_session.commit()
    db_session.refresh(session_obj)
    return session_obj


@pytest.fixture
def test_topic(db_session):
    """Create a test topic"""
    topic = Topic(
        name="Python Basics",
        description="Introduction to Python programming",
        difficulty_level="beginner"
    )
    db_session.add(topic)
    db_session.commit()
    db_session.refresh(topic)
    return topic
