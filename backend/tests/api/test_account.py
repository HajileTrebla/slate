import pytest


@pytest.mark.api
def test_create_account(client, auth_headers):

    response = client.post(
        "/accounts",
        json={
            "name": "Test Savings",
            "account_type": "asset",
            "currency": "PHP",
        },
        headers=auth_headers
    )

    assert response.status_code == 201, response.json()


@pytest.mark.api
def test_update_account(client, auth_headers):

    create_payload = {
            "name": "Test Savings",
            "account_type": "asset",
            "currency": "PHP",
        }

    account = client.post(
        "/accounts",
        json=create_payload,
        headers=auth_headers,
    )

    update_payload = {
        "name" : "Test Loan",
        "account_type": "liability",
    }

    response = client.patch(
        f"/accounts/{account.json()['uuid']}",
        json=update_payload,
        headers=auth_headers,
    )

    data = response.json()

    assert response.status_code == 200, response.json()
    assert data['name'] == 'Test Loan'
    assert data['account_type'] == 'liability'


@pytest.mark.api
def test_get_accounts(client, auth_headers):

    accounts = [
        {
            "name": "Test Savings",
            "account_type": "asset",
            "currency": "PHP",
        },
        {
            "name": "Test Loans",
            "account_type": "liability",
            "currency": "PHP",
        },
    ]

    for account in accounts:
        client.post(
            "/accounts",
            json=account,
            headers=auth_headers,
        )

    response = client.get(
        "/accounts",
        headers=auth_headers
    )

    assert len(response.json()) == 2
    assert response.status_code == 200, response.json()


@pytest.mark.api
def test_get_account(client, auth_headers):

    accounts = [
        {
            "name": "Test Savings",
            "account_type": "asset",
            "currency": "PHP",
        },
        {
            "name": "Test Loans",
            "account_type": "liability",
            "currency": "PHP",
        },
    ]

    responses = []
    for account in accounts:
        responses.append(client.post(
            "/accounts",
            json=account,
            headers=auth_headers,
        ))

    response = client.get(
        f"/accounts/{responses[0].json()["uuid"]}",
        headers=auth_headers
    )

    assert response.status_code == 200, response.json()


@pytest.mark.api
def test_get_my(client, auth_headers):

    accounts = [
        {
            "name": "Test Savings",
            "account_type": "asset",
            "currency": "PHP",
        },
        {
            "name": "Test Loans",
            "account_type": "liability",
            "currency": "PHP",
        },
    ]

    for account in accounts:
        client.post(
            "/accounts",
            json=account,
            headers=auth_headers,
        )

    response = client.get(
        "/accounts/my",
        headers=auth_headers
    )

    assert len(response.json()) == 2
    assert response.status_code == 200, response.json()
