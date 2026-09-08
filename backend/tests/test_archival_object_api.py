from fastapi.testclient import TestClient

from archive_workbench.api import app


client = TestClient(app)


def test_existing_archival_object_can_be_retrieved():
    response = client.get("/api/archival-objects/example-object")

    assert response.status_code == 200

    assert response.json() == {
        "id": "example-object",
        "representations": [
            {
                "path": "letter-front.tif",
                "integrity_status": "intact",
            },
            {
                "path": "letter-back.tif",
                "integrity_status": "modified",
            },
        ],
    }


def test_missing_archival_object_returns_not_found():
    response = client.get("/api/archival-objects/does-not-exist")

    assert response.status_code == 404