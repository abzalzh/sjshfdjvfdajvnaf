from fastapi.testclient import TestClient

from app.deps import get_db
from app.main import app
from tests.db import PASSWORD, bearer, fresh_db, get_test_db

client = TestClient(app)


def setup_function():
    # Room 1 "general": messages 1 and 3. Room 2 "homework": message 2.
    fresh_db()
    app.dependency_overrides[get_db] = get_test_db
    for name in ["Aida", "Timur"]:
        client.post("/users", json={"name": name, "password": PASSWORD})
    aida = bearer(client, "Aida")
    client.post("/rooms", json={"title": "general"})
    client.post("/rooms", json={"title": "homework"})
    client.post("/rooms/1/messages", json={"text": "hello everyone"}, headers=aida)
    client.post("/rooms/2/messages", json={"text": "the secret answer is 42"}, headers=aida)
    client.post("/rooms/1/messages", json={"text": "where is the meeting?"}, headers=aida)


def teardown_function():
    app.dependency_overrides.clear()


def search(room_id: int, q: str):
    return client.get(f"/rooms/{room_id}/search", params={"q": q})


# M1: the search keeps working for normal words

def test_search_finds_a_word():
    response = search(1, "meeting")

    assert response.status_code == 200
    assert response.json() == [{"id": 3, "text": "where is the meeting?"}]


def test_search_stays_in_its_room():
    assert search(1, "secret").json() == []


def test_an_apostrophe_is_just_a_letter():
    response = search(1, "it's")

    assert response.status_code == 200
    assert response.json() == []


# M1: the attacks find nothing

def test_or_true_does_not_open_other_rooms():
    response = search(1, "' OR 1=1 --")

    assert response.status_code == 200
    assert response.json() == []


def test_union_does_not_read_the_users_table():
    response = search(1, "zzz' UNION SELECT id, password_hash FROM users --")

    assert response.status_code == 200
    assert "argon2" not in response.text
    assert response.json() == []


def test_unknown_room_returns_404():
    response = search(99, "hello")

    assert response.status_code == 404
    assert response.json()["code"] == "room_not_found"
