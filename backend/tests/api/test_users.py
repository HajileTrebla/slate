import pytest


@pytest.mark.api
def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        }
    )

    assert response.status_code == 201, response.json()

    data = response.json()

    assert data["username"] == "j.do"
    assert data["email"] == "johndoe@gmail.com"
    assert "id" in data


@pytest.mark.api
def test_get_user(client):
    create = client.post(
        "/users",
        json={
            "username": "sam88",
            "email": "samson.g01@gmail.com",
            "password": "password123",
        }
    )

    user_id = create.json()["id"]

    response = client.get(
        f"/users/{user_id}"
    )

    assert response.status_code == 200, response.json()


@pytest.mark.api
def test_get_missing_user(client):
    response = client.get(
        "/users/999999"
    )

    assert response.status_code == 404


@pytest.mark.api
def test_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "username": "jann13",
            "email": "invalid-email",
            "password": "password123",
        }
    )

    assert response.status_code == 422
