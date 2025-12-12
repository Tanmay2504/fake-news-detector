import os

# Skip heavy model loading during tests
os.environ["SKIP_MODEL_LOAD"] = "1"

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("name") == "Fake News Detection API"
    assert "endpoints" in data


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "ok" in data
    assert "models_available" in data