from fastapi.testclient import TestClient

from app.deps import get_db
from app.main import app
from tests.db import PASSWORD, bearer, fresh_db, get_test_db

client = TestClient(app)
AIDA: dict = {}
TIMUR: dict = {}
NEW = "my-new-password-1"


def setup_function():
    fresh_db()
    app.dependency_overrides[get_db] = get_test_db
    for name in ["Aida", "Timur"]:
        client.post("/users", json={"name": name, "password": PASSWORD})
    AIDA.update(bearer(client, "Aida"))
    TIMUR.update(bearer(client, "Timur"))


def teardown_function():
    app.dependency_overrides.clear()


def login(name: str, password: str):
    return client.post("/auth/token", data={"username": name, "password": password})


# M2: your own password, nobody else's

def test_change_own_password():
    response = client.patch("/users/1/password", json={"password": NEW}, headers=AIDA)

    assert response.status_code == 204
    assert login("Aida", NEW).status_code == 200
    assert login("Aida", PASSWORD).status_code == 401


def test_change_someone_elses_password_returns_403():
    response = client.patch("/users/1/password", json={"password": NEW}, headers=TIMUR)

    assert response.status_code == 403
    assert response.json()["code"] == "not_your_account"


def test_aida_keeps_her_password_after_the_attack():
    client.patch("/users/1/password", json={"password": NEW}, headers=TIMUR)

    assert login("Aida", PASSWORD).status_code == 200
    assert login("Aida", NEW).status_code == 401


def test_unknown_id_is_403_too():
    response = client.patch("/users/99/password", json={"password": NEW}, headers=TIMUR)

    assert response.status_code == 403


def test_change_password_without_a_token_returns_401():
    response = client.patch("/users/1/password", json={"password": NEW})

    assert response.status_code == 401


def test_short_password_returns_422():
    response = client.patch("/users/1/password", json={"password": "short"}, headers=AIDA)

    assert response.status_code == 422
