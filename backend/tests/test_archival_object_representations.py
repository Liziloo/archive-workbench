from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone

from archive_workbench.archival_object import create_archival_object


def test_one_archival_object_can_have_multiple_digital_representations(
    tmp_path: Path,
):
    first_scan = tmp_path / "letter-front.tif"
    second_scan = tmp_path / "letter-back.tif"

    first_scan.write_bytes(b"front of the letter")
    second_scan.write_bytes(b"back of the letter")

    physical_object = create_archival_object()

    first_representation = physical_object.add_representation(first_scan)
    second_representation = physical_object.add_representation(second_scan)

    representations = physical_object.representations

    assert len(representations) == 2
    assert first_representation in representations
    assert second_representation in representations
    assert first_representation != second_representation

    assert first_scan.read_bytes() == b"front of the letter"
    assert second_scan.read_bytes() == b"back of the letter"

def test_identical_files_are_detected_as_duplicates(tmp_path: Path):
    first_scan = tmp_path / "letter-front.tif"
    renamed_scan = tmp_path / "letter-front-renamed.tif"

    first_scan.write_bytes(b"front of the letter")
    renamed_scan.write_bytes(b"front of the letter")

    physical_object = create_archival_object()

    physical_object.add_representation(first_scan)

    result = physical_object.check_for_duplicate(renamed_scan)

    assert result is True

def test_duplicate_requires_confirmation_before_being_added(tmp_path: Path):
    first_scan = tmp_path / "letter-front.tif"
    renamed_scan = tmp_path / "letter-front-renamed.tif"

    first_scan.write_bytes(b"front of the letter")
    renamed_scan.write_bytes(b"front of the letter")

    physical_object = create_archival_object()
    physical_object.add_representation(first_scan)

    result = physical_object.add_representation(renamed_scan)

    assert result.duplicate is True
    assert result.added is False
    assert len(physical_object.representations) == 1

    result = physical_object.add_representation(
        renamed_scan,
        confirm_duplicate=True,
    )

    assert result.duplicate is True
    assert result.added is True
    assert len(physical_object.representations) == 2

def test_different_digital_representations_are_not_duplicates(
    tmp_path: Path,
):
    first_scan = tmp_path / "letter-front.tif"
    second_scan = tmp_path / "letter-back.tif"

    first_scan.write_bytes(b"front of the letter")
    second_scan.write_bytes(b"back of the letter")

    physical_object = create_archival_object()

    physical_object.add_representation(first_scan)

    result = physical_object.add_representation(second_scan)

    assert result.duplicate is False
    assert result.added is True
    assert len(physical_object.representations) == 2

def test_representation_has_stable_content_identity(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    content = b"front of the letter"
    scan.write_bytes(content)

    physical_object = create_archival_object()

    result = physical_object.add_representation(scan)

    assert result.added is True
    assert result.representation.identity == sha256(content).hexdigest()

def test_same_content_at_different_path_is_detected_as_duplicate(
    tmp_path: Path,
):
    original_scan = tmp_path / "original" / "letter-front.tif"
    relocated_scan = tmp_path / "relocated" / "renamed-letter-front.tif"

    original_scan.parent.mkdir()
    relocated_scan.parent.mkdir()

    content = b"front of the letter"
    original_scan.write_bytes(content)
    relocated_scan.write_bytes(content)

    physical_object = create_archival_object()

    physical_object.add_representation(original_scan)

    result = physical_object.add_representation(relocated_scan)

    assert result.duplicate is True
    assert result.added is False
    assert len(physical_object.representations) == 1

def test_archival_object_exposes_its_digital_representations(
    tmp_path: Path,
):
    first_scan = tmp_path / "letter-front.tif"
    second_scan = tmp_path / "letter-back.tif"

    first_scan.write_bytes(b"front of the letter")
    second_scan.write_bytes(b"back of the letter")

    physical_object = create_archival_object()

    first_result = physical_object.add_representation(first_scan)
    second_result = physical_object.add_representation(second_scan)

    representations = physical_object.representations

    assert first_result.representation in representations
    assert second_result.representation in representations
    assert len(representations) == 2

def test_representation_records_when_it_was_added(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"front of the letter")

    physical_object = create_archival_object()

    before = datetime.now(timezone.utc)
    result = physical_object.add_representation(scan)
    after = datetime.now(timezone.utc)

    assert result.added is True
    assert before <= result.representation.added_at <= after

def test_representation_records_last_known_path(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"front of the letter")

    physical_object = create_archival_object()

    result = physical_object.add_representation(scan)

    assert result.added is True
    assert result.representation.path == scan

def test_representation_detects_when_file_has_changed(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    scan.write_bytes(b"changed content")

    assert result.representation.matches_current_file() is False

def test_representation_detects_when_file_is_missing(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    scan.unlink()

    assert result.representation.matches_current_file() is False