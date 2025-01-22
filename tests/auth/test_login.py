import pytest
from fastapi.testclient import TestClient
from app.main import app
import urllib.parse

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c

@pytest.fixture(scope="module")
def as_admin():
    return {"username": "admin", "password": "admin"}

@pytest.fixture(scope="module")
def as_user():
    return {"username": "user", "password": "user"}

def test_login(client, as_admin):
    urlparams = urllib.parse.urlencode(as_admin)

    response = client.post("/auth/login?" + urlparams)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token