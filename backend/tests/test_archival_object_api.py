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

    # New format includes path, identity, duplicate, added (integrity_status is removed)
    rep = response.json()["representations"][-1]
    assert rep["path"] == str(representation_path)
    assert "identity" in rep
    assert isinstance(rep["duplicate"], bool)
    assert rep["added"] is True


def test_duplicate_representation_is_rejected_at_api_level(tmp_path):
    # Create a file with specific content so SHA-256 identity is known
    content = b"identical file contents for duplicate test"
    dup_file = tmp_path / "dup-file.tif"
    dup_file.write_bytes(content)

    # First copy — should succeed with 200
    response1 = client.post(
        "/api/archival-objects/example-object/representations",
        json={"path": str(dup_file)},
    )
    assert response1.status_code == 200
    reps_after_first = response1.json()["representations"]
    assert len(reps_after_first) == 1
    assert reps_after_first[0]["added"] is True

    # Second copy with the same file (identical content) — should fail with 409
    response2 = client.post(
        "/api/archival-objects/example-object/representations",
        json={"path": str(dup_file)},
    )
    assert response2.status_code == 409

    # The representations list should still only contain the first copy
    reps_after_second = response2.json()["representations"]
    assert len(reps_after_second) == 1


def test_add_representation_response_includes_identity(tmp_path):
    representation_path = tmp_path / "file-with-identity.tif"
    representation_path.write_bytes(b"digital file contents")

    response = client.post(
        "/api/archival-objects/example-object/representations",
        json={"path": str(representation_path)},
    )

    assert response.status_code == 200

    for rep in response.json()["representations"]:
        identity = rep["identity"]
        assert isinstance(identity, str)
        assert len(identity) == 64  # SHA-256 hex digest is always 64 characters