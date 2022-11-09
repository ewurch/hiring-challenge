from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/v1/")
    assert response.status_code == 200