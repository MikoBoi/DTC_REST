import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.auth.test_login import test_login, client, as_admin



def test_create_order(client, as_admin):
    token = test_login(client, as_admin)
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_name": "Test",
            "products": [{"name": "Test Product", "price": 100, "quantity": 2}]
        },
        headers={"token": token}
    )
    assert response.status_code == 200
    assert response.json()[0]["customer_name"] == "Test"
    return response

def test_create_order_unauthorized(client):
    response = client.post(
        "/api/v1/orders/",
        json={
            "customer_name": "Test",
            "products": [{"name": "Test Product", "price": 100, "quantity": 2}]
        },
        headers={"token": "WRONG_TOKEN"}
    )
    assert response.status_code == 401

def test_create_order_field_validation(client, as_admin):
    token = test_login(client, as_admin)
    response = client.post(
        "/api/v1/orders/",
        json={
            "customer_name": "Test",
            # "products": [{"name": "Test Product", "price": 100, "quantity": 2}]
        },
        headers={"token": token}
    )
    assert response.status_code == 422