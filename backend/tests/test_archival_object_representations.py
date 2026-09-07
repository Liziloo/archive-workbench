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

def test_representation_reports_when_file_has_been_modified(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    scan.write_bytes(b"changed content")

    assert result.representation.integrity_status == "modified"

def test_representation_reports_when_file_is_missing(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    scan.unlink()

    assert result.representation.integrity_status == "missing"

def test_representation_reports_when_file_is_intact(tmp_path: Path):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    assert result.representation.integrity_status == "intact"

def test_archival_object_identifies_representation_needing_attention(
    tmp_path: Path,
):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    scan.write_bytes(b"changed content")

    assert result.representation in physical_object.representations_needing_attention

def test_archival_object_does_not_identify_intact_representation_as_needing_attention(
    tmp_path: Path,
):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    assert result.representation not in physical_object.representations_needing_attention

def test_representation_can_be_explicitly_checked_for_integrity(
    tmp_path: Path,
):
    scan = tmp_path / "letter-front.tif"
    scan.write_bytes(b"original content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(scan)

    scan.write_bytes(b"changed content")

    assert result.representation.check_integrity() == "modified"

def test_representation_can_find_matching_file_in_search_location(
    tmp_path: Path,
):
    original = tmp_path / "original" / "letter-front.tif"
    recovered = tmp_path / "somewhere-else" / "renamed-letter-front.tif"

    original.parent.mkdir()
    recovered.parent.mkdir()

    content = b"original content"
    original.write_bytes(content)
    recovered.write_bytes(content)

    physical_object = create_archival_object()
    result = physical_object.add_representation(original)

    original.unlink()

    matches = result.representation.find_matching_files(tmp_path)

    assert recovered in matches

def test_representation_finds_all_matching_files_in_search_location(
    tmp_path: Path,
):
    original = tmp_path / "original" / "letter-front.tif"
    first_copy = tmp_path / "copy-one" / "letter-front-copy.tif"
    second_copy = tmp_path / "copy-two" / "letter-front-backup.tif"

    original.parent.mkdir()
    first_copy.parent.mkdir()
    second_copy.parent.mkdir()

    content = b"original content"
    original.write_bytes(content)
    first_copy.write_bytes(content)
    second_copy.write_bytes(content)

    physical_object = create_archival_object()
    result = physical_object.add_representation(original)

    original.unlink()

    matches = result.representation.find_matching_files(tmp_path)

    assert set(matches) == {first_copy, second_copy}

def test_representation_can_verify_a_selected_matching_file(
    tmp_path: Path,
):
    original = tmp_path / "original" / "letter-front.tif"
    candidate = tmp_path / "somewhere-else" / "renamed-letter-front.tif"

    original.parent.mkdir()
    candidate.parent.mkdir()

    content = b"original content"
    original.write_bytes(content)
    candidate.write_bytes(content)

    physical_object = create_archival_object()
    result = physical_object.add_representation(original)

    original.unlink()

    assert result.representation.verify_file(candidate) is True

def test_representation_can_be_reassociated_with_verified_file(
    tmp_path: Path,
):
    original = tmp_path / "original" / "letter-front.tif"
    recovered = tmp_path / "somewhere-else" / "renamed-letter-front.tif"

    original.parent.mkdir()
    recovered.parent.mkdir()

    content = b"original content"
    original.write_bytes(content)
    recovered.write_bytes(content)

    physical_object = create_archival_object()
    result = physical_object.add_representation(original)

    original.unlink()

    assert result.representation.reassociate_file(recovered) is True
    assert result.representation.path == recovered

def test_representation_refuses_to_be_reassociated_with_nonmatching_file(
    tmp_path: Path,
):
    original = tmp_path / "original" / "letter-front.tif"
    wrong_file = tmp_path / "somewhere-else" / "different-letter.tif"

    original.parent.mkdir()
    wrong_file.parent.mkdir()

    original.write_bytes(b"original content")
    wrong_file.write_bytes(b"different content")

    physical_object = create_archival_object()
    result = physical_object.add_representation(original)

    original.unlink()

    assert result.representation.reassociate_file(wrong_file) is False
    assert result.representation.path == original

def test_representations_can_have_an_explicit_order(tmp_path):
    first = tmp_path / "page-one.txt"
    second = tmp_path / "page-two.txt"
    third = tmp_path / "page-three.txt"

    first.write_text("page one")
    second.write_text("page two")
    third.write_text("page three")

    physical_object = create_archival_object()

    first_result = physical_object.add_representation(first)
    second_result = physical_object.add_representation(second)
    third_result = physical_object.add_representation(third)

    first_result.representation.set_order(1)
    second_result.representation.set_order(2)
    third_result.representation.set_order(3)

    assert physical_object.ordered_representations == [
        first_result.representation,
        second_result.representation,
        third_result.representation,
    ]


def test_representations_do_not_require_an_order(tmp_path):
    first = tmp_path / "photo-one.jpg"
    second = tmp_path / "photo-two.jpg"

    first.write_bytes(b"photo one")
    second.write_bytes(b"photo two")

    physical_object = create_archival_object()

    first_result = physical_object.add_representation(first)
    second_result = physical_object.add_representation(second)

    assert first_result.representation.order is None
    assert second_result.representation.order is None