from email import header
from urllib import response

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