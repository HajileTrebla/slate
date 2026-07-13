import pytest


@pytest.mark.api
def test_username_login(client):

    create = client.post(
        "/users",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        }
    )

    identifier = create.json()["username"]
    response = client.post(
        "/auth/login",
        json={
            "identifier": identifier,
            "password": "password123",
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.api
def test_email_login(client):

    create = client.post(
        "/users",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        }
    )

    identifier = create.json()["email"]
    response = client.post(
        "/auth/login",
        json={
            "identifier": identifier,
            "password": "password123",
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.api
def test_invalid_credentials(client):

    response = client.post(
        "/auth/login",
        json={
            "identifier": "invalid@example.com",
            "password": "password1222",
        }
    )

    assert response.status_code == 401, response.json()
