from fastapi.testclient import TestClient
from devops_project.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"project": "I am learning DevOps"}