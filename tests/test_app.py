import pytest
from app import create_app, db
from app.config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    WTF_CSRF_ENABLED = False


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_register_and_login(client):
    resp = client.post("/register", data={
        "username": "testuser", "email": "test@example.com", "password": "pass123"
    }, follow_redirects=True)
    assert resp.status_code == 200

    resp = client.post("/login", data={"username": "testuser", "password": "pass123"}, follow_redirects=True)
    assert b"Welcome back" in resp.data


def test_unauthenticated_api_redirects(client):
    resp = client.get("/api/tasks")
    assert resp.status_code in (302, 401)
