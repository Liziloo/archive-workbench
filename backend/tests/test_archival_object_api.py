import pytest
from fastapi.testclient import TestClient

from archive_workbench import api
from archive_workbench.api import app


@pytest.fixture(autouse=True)
def reset_archival_objects():
    api._archival_objects = {
        "example-object": {
            "id": "example-object",
            "representations": [
                {"path": "letter-front.tif", "integrity_status": "intact"},
                {"path": "letter-back.tif", "integrity_status": "modified"},
            ],
        }
    }


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


def test_digital_representation_can_be_added_to_an_existing_archival_object(
    tmp_path,
):
    representation_path = tmp_path / "letter-envelope.tif"
    representation_path.write_bytes(b"letter envelope contents")

    response = client.post(
        "/api/archival-objects/example-object/representations",
        json={"path": str(representation_path)},
    )

    assert response.status_code == 200

    assert response.json()["representations"][-1] == {
        "path": str(representation_path),
        "integrity_status": "intact",
    }