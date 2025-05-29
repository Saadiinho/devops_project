from fastapi.testclient import TestClient
from devops_project.main import app
from devops_project.main import __version__

client = TestClient(app)


def test_read_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {
        "name": "devops_project API",
        "version": __version__,
        "status": {
            "application": "running",
            "database": "Unsuccessful connection: 2005 (HY000): Unknown MySQL server host 'mysql' (-3)",
        },
    }


def test_education_name_logo():
    response = client.get("/education-name-logo")
    assert response.status_code == 200
    