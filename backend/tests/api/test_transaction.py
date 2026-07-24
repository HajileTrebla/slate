import pytest
import uuid


@pytest.mark.api
def test_create_transaction(
    client,
    auth_headers,
    account_factory,
):
    cash = account_factory(name="Cash")
    revenue = account_factory(name="Revenue")

    response = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "date": "2026-07-24T10:00:00",
            "description": "Sale",
            "reference": "INV-001",
            "entries": [
                {
                    "account_id": str(cash.uuid),
                    "debit": "100.00",
                },
                {
                    "account_id": str(revenue.uuid),
                    "credit": "100.00",
                },
            ],
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["description"] == "Sale"
    assert body["reference"] == "INV-001"
    assert len(body["entries"]) == 2


@pytest.mark.api
def test_get_transaction(
    client,
    auth_headers,
    transaction_factory,
):
    transaction = transaction_factory()

    response = client.get(
        f"/transactions/{transaction.uuid}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["uuid"] == str(transaction.uuid)


@pytest.mark.api
def test_get_transactions(
    client,
    auth_headers,
    transaction_factory,
):
    transaction_factory()
    transaction_factory()

    response = client.get(
        "/transactions/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 2


@pytest.mark.api
def test_update_transaction(
    client,
    auth_headers,
    transaction_factory,
):
    transaction = transaction_factory()

    response = client.patch(
        f"/transactions/{transaction.uuid}",
        headers=auth_headers,
        json={
            "description": "Updated Description",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["description"] == "Updated Description"


@pytest.mark.api
def test_get_transaction_not_found(
    client,
    auth_headers,
):
    response = client.get(
        f"/transactions/{uuid.uuid4()}",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.api
def test_create_unbalanced_transaction(
    client,
    auth_headers,
    account_factory,
):
    cash = account_factory(name="Cash")
    revenue = account_factory(name="Revenue")

    response = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "date": "2026-07-24T10:00:00",
            "description": "Sale",
            "reference": "INV-001",
            "entries": [
                {
                    "account_id": str(cash.uuid),
                    "debit": "100.00",
                },
                {
                    "account_id": str(revenue.uuid),
                    "credit": "50.00",
                },
            ],
        },
    )

    assert response.status_code == 201


def test_transaction_requires_two_entries(
    client,
    auth_headers,
    account_factory,
):
    cash = account_factory(name="Cash")

    response = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "date": "2026-07-24T10:00:00",
            "description": "Sale",
            "reference": "INV-001",
            "entries": [
                {
                    "account_id": str(cash.uuid),
                    "debit": "100.00",
                }
            ],
        },
    )

    assert response.status_code == 400


def test_transaction_invalid_account(
    client,
    auth_headers,
):
    response = client.post(
        "/transactions/",
        headers=auth_headers,
        json={
            "date": "2026-07-24T10:00:00",
            "description": "Sale",
            "reference": "INV-001",
            "entries": [
                {
                    "account_id": str(uuid.uuid4()),
                    "debit": "100.00",
                },
                {
                    "account_id": str(uuid.uuid4()),
                    "credit": "100.00",
                },
            ],
        },
    )

    assert response.status_code == 404