from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_phase1_search_jobs_rejects_missing_files():
    response = client.post("/phase1/search-jobs", files=[])
    assert response.status_code in {400, 422}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
