import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.auth.test_login import test_login, client, as_admin, as_user



def test_edit_order_as_admin(client, as_admin):
    token = test_login(client, as_admin)
    response = client.put(
        "/api/v1/orders/7",
        json={
            "status": "cancelled",
            "products": [{"name": "TEST_PRD_ADM", "price": 1000, "quantity": 2}]
        },
        headers={"token": token}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

def test_edit_order_as_user(client, as_user):
    token = test_login(client, as_user)
    response = client.put(
        "/api/v1/orders/3",
        json={
            "status": "confirmed",
            "products": [{"name": "TEST_PRD_USR", "price": 1000, "quantity": 2}]
        },
        headers={"token": token}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"

def test_edit_order_as_user_forbidden(client, as_user):
    token = test_login(client, as_user)
    response = client.put(
        "/api/v1/orders/1",
        json={
            "status": "confirmed",
            "products": [{"name": "TEST_PRD_USR", "price": 1000, "quantity": 2}]
        },
        headers={"token": token}
    )
    assert response.status_code == 403

def test_edit_order_as_admin_not_found(client, as_admin):
    token = test_login(client, as_admin)
    response = client.put(
        "/api/v1/orders/6",
        json={
            "status": "confirmed",
            "products": [{"name": "TEST_PRD_USR", "price": 1000, "quantity": 2}]
        },
        headers={"token": token}
    )
    assert response.status_code == 404

def test_edit_order_unauthorized(client):
    response = client.put(
        "/api/v1/orders/6",
        json={
            "status": "confirmed",
            "products": [{"name": "TEST_PRD_USR", "price": 1000, "quantity": 2}]
        },
        headers={"token": "WRONG_TOKEN"}
    )
    assert response.status_code == 401