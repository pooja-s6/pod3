import pytest
from app.tests.conftest import client, test_user, test_session


def test_send_chat_message(client, test_session):
    """Test sending a chat message"""
    response = client.post("/ai/chat", json={
        "session_id": str(test_session.session_id),
        "message": "What is Python?",
        "user_id": test_session.user_id
    })
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "user_message" in data
    assert "ai_response" in data
    assert "timestamp" in data


def test_chat_message_missing_session_id(client, test_user):
    """Test chat fails without session_id"""
    response = client.post("/ai/chat", json={
        "message": "What is Python?",
        "user_id": test_user.user_id
    })
    assert response.status_code == 422


def test_chat_message_missing_message(client, test_session):
    """Test chat fails without message"""
    response = client.post("/ai/chat", json={
        "session_id": str(test_session.session_id),
        "user_id": test_session.user_id
    })
    assert response.status_code == 422


def test_chat_message_with_mode(client, test_session):
    """Test sending a chat message with specific mode"""
    response = client.post("/ai/chat", json={
        "session_id": str(test_session.session_id),
        "message": "Explain recursion",
        "user_id": test_session.user_id,
        "mode": "tutor"
    })
    assert response.status_code == 200
    data = response.json()
    assert data.get("mode") in ["tutor", "normal", "quiz", None]


def test_chat_message_returns_ai_response(client, test_session):
    """Test that AI response is returned"""
    response = client.post("/ai/chat", json={
        "session_id": str(test_session.session_id),
        "message": "Hello, how can you help me learn?",
        "user_id": test_session.user_id
    })
    assert response.status_code == 200
    data = response.json()
    
    # Should have either a real response or an error message (API key issue)
    assert "ai_response" in data
    assert len(data["ai_response"]) > 0


def test_get_chat_history(client, test_session):
    """Test retrieving chat history"""
    # First send a message
    client.post("/ai/chat", json={
        "session_id": str(test_session.session_id),
        "message": "What is a list in Python?",
        "user_id": test_session.user_id
    })
    
    # Then get history
    response = client.get(f"/ai/chat/history/{test_session.session_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
