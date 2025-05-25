from fastapi.testclient import TestClient
from devops_project.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {
        "name": "devops_project API",
        "version": "1.0.0",
        "status": "running",
    }
