import pytest


@pytest.mark.api
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        },
    )

    data = response.json()

    assert response .status_code == 200, response.json()

    assert "id" in data["user"]
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "j.do"
    assert data["user"]["email"] == "johndoe@gmail.com"


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
def test_me(client):
    client.post(
        "/auth/register",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "identifier": "j.do",
            "password": "password123",
        }
    )

    token = response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200, response.json()


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


@pytest.mark.api
def test_duplicate_username_registration(client):
    client.post(
        "/auth/register",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "j.do",
            "email": None,
            "password": "password123",
        },
    )

    assert response.status_code == 400, response.json()


@pytest.mark.api
def test_duplicate_email_registration(client):
    client.post(
        "/auth/register",
        json={
            "username": "j.do",
            "email": "johndoe@gmail.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "jonD",
            "email": "johndoe@gmail.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400, response.json()


@pytest.mark.api
def test_me_requires_auth(client):
    response = client.get(
        "/auth/me"
    )

    assert response.status_code == 401, response.json()


@pytest.mark.api
def test_me_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalidtoken"
        }
    )

    assert response.status_code == 401, response.json()
