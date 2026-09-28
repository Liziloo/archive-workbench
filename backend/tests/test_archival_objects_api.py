import pytest
from fastapi.testclient import TestClient
from archive_workbench import api
from archive_workbench.api import app

import uuid as uuid_module


@pytest.fixture
def reset_store():
    """Reset the in-memory store to the default state (example-object only)."""
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


def test_archival_objects_can_be_listed(reset_store):
    """GET /api/archival-objects returns all objects."""
    response = client.get("/api/archival-objects")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1
    # At minimum, example-object exists
    ids = [item["id"] for item in items]
    assert "example-object" in ids
    # Each item has summary info
    for item in items:
        assert "id" in item
        assert "representation_count" in item


def test_create_archival_object_returns_new_id(reset_store):
    """POST /api/archival-objects returns a new unique object."""
    response = client.post("/api/archival-objects")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    # The ID should be a valid UUID format
    new_id = data["id"]
    parsed = uuid_module.UUID(new_id)  # will raise if not valid UUID
    assert isinstance(parsed, uuid_module.UUID)


def test_created_archival_object_appears_in_list(reset_store):
    """After creating an object, it appears in the list."""
    create_resp = client.post("/api/archival-objects")
    new_id = create_resp.json()["id"]

    list_resp = client.get("/api/archival-objects")
    ids = [item["id"] for item in list_resp.json()]
    assert new_id in ids


def test_create_archival_object_returns_summary_with_zero_representations(reset_store):
    """Created object reports 0 representations."""
    response = client.post("/api/archival-objects")
    data = response.json()
    assert data["representation_count"] == 0


def test_list_response_contains_all_created_objects_not_just_example_object(reset_store):
    """The list includes multiple objects, not just the default example-object."""
    ids_to_create = []
    for _ in range(3):
        resp = client.post("/api/archival-objects")
        ids_to_create.append(resp.json()["id"])

    list_resp = client.get("/api/archival-objects")
    ids = [item["id"] for item in list_resp.json()]

    assert "example-object" in ids
    for new_id in ids_to_create:
        assert new_id in ids


def test_create_then_add_representation_works_end_to_end(reset_store, tmp_path):
    """Create a new object, then add a representation to it."""
    # Create a new archival object
    create_resp = client.post("/api/archival-objects")
    object_id = create_resp.json()["id"]

    # Add a file representation
    file_path = tmp_path / "new-object-photo.tif"
    file_path.write_bytes(b"photo contents here")

    rep_resp = client.post(
        f"/api/archival-objects/{object_id}/representations",
        json={"path": str(file_path)},
    )
    assert rep_resp.status_code == 200

    # Verify it's retrievable
    get_resp = client.get(f"/api/archival-objects/{object_id}")
    assert get_resp.status_code == 200

    # Verify representation appears in list summary
    list_resp = client.get("/api/archival-objects")
    item = next(it for it in list_resp.json() if it["id"] == object_id)
    assert item["representation_count"] >= 1


def test_created_archival_object_has_empty_representation_list(reset_store):
    """A newly created object starts with no representations."""
    create_resp = client.post("/api/archival-objects")
    object_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/archival-objects/{object_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["representations"] == []
