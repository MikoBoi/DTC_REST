import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.auth.test_login import test_login, client, as_admin, as_user
from tests.test_order_endpoints.test_create_order import test_create_order



def test_delete_order_as_admin(client, as_admin):
    create_for_delete = test_create_order(client, as_admin)
    id = create_for_delete.json()[1]["order_id"]

    token = test_login(client, as_admin)
    response = client.delete(
        "/api/v1/orders/"+str(id),
        headers={"token": token}
    )
    assert response.status_code == 200
    assert response.json()["is_deleted"] == True

def test_delete_order_as_user_forbidden(client, as_admin, as_user):
    create_for_delete = test_create_order(client, as_admin)
    id = create_for_delete.json()[1]["order_id"]

    token = test_login(client, as_user)
    response = client.delete(
        "/api/v1/orders/"+str(id),
        headers={"token": token}
    )
    assert response.status_code == 403

def test_delete_order_as_admin_not_found(client, as_admin):
    token = test_login(client, as_admin)
    response = client.delete(
        "/api/v1/orders/6",
        headers={"token": token}
    )
    assert response.status_code == 404

def test_delete_order_unauthorized(client):
    response = client.put(
        "/api/v1/orders/1",
        json={
            "status": "confirmed",
            "products": [{"name": "TEST_PRD_USR", "price": 1000, "quantity": 2}]
        },
        headers={"token": "WRONG_TOKEN"}
    )
    assert response.status_code == 401