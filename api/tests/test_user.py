from api.controllers.user import get_user_id
from api.db.models import User, UserView
from fastapi.testclient import TestClient
from main import app
from api.tests.mock_session import mock_db_session
import pytest

client = TestClient(app)


@pytest.fixture
def token():
    form_data = {"username": "test", "password": "secret"}
    response = client.post("/token", data=form_data)
    assert response.status_code == 200
    return response.json()["access_token"]


def test_get_user_me(token):
    headers = {"Authorization": f"Bearer {str(token)}"}
    response = client.get("/api/users/me", headers=headers)
    data = {
        "username": "test",
        "hashed_password": "$2b$12$xXgZtEnOJxiEHxRAU2Vu0eDihgQ3sRv2JM5YLMKGf7FJgiFysRTkW",
        "full_name": "Testing App",
        "city": "New York",
        "phone_number": "123456789",
        "email": "test@example.com",
        "id": 1,
        "age": 30,
        "country": "USA",
        "is_active": True,
    }
    assert response.status_code == 200
    assert response.json() == data


def test_get_user_me_without_token():
    response = client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_user(token, mock_db_session):
    new_user_data = {
        "id": 1,
        "username": "testuser1",
        "hashed_password": "secret",
        "email": "testuser1@example.com",
        "full_name": "Test User",
        "age": 30,
        "city": "New York",
        "country": "USA",
        "phone_number": "123456789",
        "is_active": True,
    }
    headers = {"Authorization": f"Bearer {str(token)}"}
    response = client.post("/api/users/", headers=headers, json=new_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser1"
    assert data["email"] == "testuser1@example.com"
    assert data["full_name"] == "Test User"
    assert data["age"] == 30
    assert data["city"] == "New York"
    assert data["country"] == "USA"
    assert data["phone_number"] == "123456789"
    assert data["is_active"] == True
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


def test_get_users(token, mock_db_session):
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        User(id=2, username="user1", email="user1@example.com", full_name="User One"),
        User(id=3, username="user2", email="user2@example.com", full_name="User Two"),
    ]
    headers = {"Authorization": f"Bearer {str(token)}"}
    response = client.get("/api/users/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) == 2
    assert data["result"][0]["username"] == "user1"
    assert data["result"][0]["email"] == "user1@example.com"
    assert data["result"][0]["full_name"] == "User One"
    assert data["result"][1]["username"] == "user2"
    assert data["result"][1]["email"] == "user2@example.com"
    assert data["result"][1]["full_name"] == "User Two"


""" def test_update_user(token, mock_db_session):
    existing_user_id = 1
    existing_user_data = {
        "username": "existing_user",
        "email": "existing_user@example.com",
        "hashed_password": "Existing User",
    }
    mock_db_session.query().filter_by().first.return_value = User(
        id=existing_user_id, **existing_user_data
    )

    user_update_data = {
        "email": "updated_email@example.com",
        "full_name": "Updated User",
    }

    headers = {"Authorization": f"Bearer {str(token)}"}
    response = client.put(
        f"/api/users/{existing_user_id}", headers=headers, json=user_update_data
    )
    assert response.status_code == 200

    updated_user_data = response.json()
    assert updated_user_data["email"] == "updated_email@example.com"
    assert updated_user_data["full_name"] == "Updated User"

    mock_db_session.query().filter_by().first.assert_called_once()
    mock_db_session.commit.assert_called_once() """


def test_delete_user(token, mock_db_session):
    existing_user_id = 1
    existing_user_data = {
        "username": "existing_user",
        "email": "existing_user@example.com",
        "full_name": "Existing User",
    }
    mock_db_session.query().filter_by().first.return_value = User(
        id=existing_user_id, **existing_user_data
    )

    headers = {"Authorization": f"Bearer {str(token)}"}
    response = client.delete(f"/api/users/{existing_user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    mock_db_session.delete.assert_called_once()
