from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
