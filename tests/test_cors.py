from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SITE = "http://127.0.0.1:5500"          # web/index.html, served by python -m http.server 5500
OTHER = "http://evil.example"


def preflight(origin: str):
    # What a browser sends before a POST with a JSON body from another site
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "authorization,content-type",
    }
    return client.options("/rooms/1/messages", headers=headers)


# M3: CORSMiddleware with a fixed list of sites

def test_preflight_from_our_site_is_allowed():
    response = preflight(SITE)

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == SITE


def test_preflight_from_another_site_is_refused():
    response = preflight(OTHER)

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_simple_get_from_our_site_gets_the_header():
    response = client.get("/rooms", headers={"Origin": SITE})

    assert response.headers["access-control-allow-origin"] == SITE


def test_cors_does_not_block_a_client_without_a_browser():
    # No browser, no CORS: the server answers anyway. CORS is not a lock on the API.
    response = client.get("/rooms", headers={"Origin": OTHER})

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
