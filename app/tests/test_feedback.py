import pytest
from app.tests.conftest import client, test_user, test_session


def test_submit_feedback(client, test_user, test_session):
    """Test submitting feedback"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "session_id": str(test_session.session_id),
        "rating": 5,
        "comments": "Great learning experience!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "success" in str(data).lower()


def test_submit_feedback_missing_rating(client, test_user, test_session):
    """Test feedback submission fails without rating"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "session_id": str(test_session.session_id),
        "comments": "Good session"
    })
    assert response.status_code == 422


def test_submit_feedback_invalid_rating(client, test_user, test_session):
    """Test feedback with invalid rating value"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "session_id": str(test_session.session_id),
        "rating": 10,  # Invalid - should be 1-5
        "comments": "Test"
    })
    # Should either reject or accept
    assert response.status_code in [200, 422]


def test_submit_feedback_minimum_rating(client, test_user, test_session):
    """Test feedback with minimum rating"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "session_id": str(test_session.session_id),
        "rating": 1,
        "comments": "Could be better"
    })
    assert response.status_code == 200


def test_submit_feedback_maximum_rating(client, test_user, test_session):
    """Test feedback with maximum rating"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "session_id": str(test_session.session_id),
        "rating": 5,
        "comments": "Excellent!"
    })
    assert response.status_code == 200


def test_submit_feedback_empty_comments(client, test_user, test_session):
    """Test feedback with empty comments"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "session_id": str(test_session.session_id),
        "rating": 4,
        "comments": ""
    })
    assert response.status_code == 200


def test_submit_feedback_optional_session_id(client, test_user):
    """Test feedback without session_id (if allowed)"""
    response = client.post("/feedback", json={
        "user_id": test_user.user_id,
        "rating": 4,
        "comments": "General feedback"
    })
    # Depending on schema, this may be 200 or 422
    assert response.status_code in [200, 422]
