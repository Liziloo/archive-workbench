from pathlib import Path

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
