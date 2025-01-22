import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.auth.test_login import test_login, client, as_admin, as_user



def test_get_orders_as_admin(client, as_admin):
    token = test_login(client, as_admin)
    response = client.get(
        "/api/v1/orders",
        headers={"token": token}
    )
    assert response.status_code == 200

def test_get_order_as_admin(client, as_admin):
    token = test_login(client, as_admin)
    response = client.get(
        "/api/v1/orders/3",
        headers={"token": token}
    )
    assert response.status_code == 200

def test_get_order_as_admin_not_found(client, as_admin):
    token = test_login(client, as_admin)
    response = client.get(
        "/api/v1/orders/4",
        headers={"token": token}
    )
    assert response.status_code == 404

def test_get_orders_as_user(client, as_user):
    token = test_login(client, as_user)
    response = client.get(
        "/api/v1/orders",
        headers={"token": token}
    )
    assert response.status_code == 200

def test_get_order_as_user(client, as_user):
    token = test_login(client, as_user)
    response = client.get(
        "/api/v1/orders/7",
        headers={"token": token}
    )
    assert response.status_code == 200

def test_get_order_as_user_not_found(client):
    token = test_login(client, {"username": "user", "password": "user"})
    response = client.get(
        "/api/v1/orders/6",
        headers={"token": token}
    )
    assert response.status_code == 404

def test_get_order_as_user_forbidden(client):
    token = test_login(client, {"username": "user", "password": "user"})
    response = client.get(
        "/api/v1/orders/1",
        headers={"token": token}
    )
    assert response.status_code == 403

def test_get_order_unauthorized(client):
    response = client.get(
        "/api/v1/orders/1",
        headers={"token": "WRONG_TOKEN"}
    )
    assert response.status_code == 401