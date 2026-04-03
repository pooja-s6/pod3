import pytest
from app.tests.conftest import client, test_user


def test_create_session(client, test_user):
    """Test creating a new session"""
    response = client.post("/session/create", json={
        "user_id": test_user.user_id,
        "topic": "Python Basics"
    })
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["user_id"] == test_user.user_id
    assert data["topic"] == "Python Basics"


def test_create_session_missing_user_id(client):
    """Test session creation fails without user_id"""
    response = client.post("/session/create", json={
        "topic": "Python Basics"
    })
    assert response.status_code == 422  # Validation error


def test_create_session_with_optional_fields(client, test_user):
    """Test session creation with optional fields"""
    response = client.post("/session/create", json={
        "user_id": test_user.user_id,
        "topic": "Advanced Python",
        "difficulty_level": "advanced"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Advanced Python"


def test_session_returns_uuid(client, test_user):
    """Test that session_id is a valid UUID"""
    import uuid
    response = client.post("/session/create", json={
        "user_id": test_user.user_id,
        "topic": "Python Basics"
    })
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # Verify it's a valid UUID
    try:
        uuid.UUID(str(session_id))
    except ValueError:
        pytest.fail(f"session_id {session_id} is not a valid UUID")
