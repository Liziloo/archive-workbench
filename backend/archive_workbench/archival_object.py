from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone


def _file_hexdigest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _file_digest(path: Path) -> bytes:
    return sha256(path.read_bytes()).digest()


class Representation:
    def __init__(self, path: Path, duplicate: bool, added: bool):
        self.path = path
        self.duplicate = duplicate
        self.added = added
        self.identity = _file_hexdigest(path)
        self.representation = self
        self.added_at = datetime.now(timezone.utc)
        self.order = None

    def read_bytes(self):
        return self.path.read_bytes()

    def matches_current_file(self):
        try:
            current_hash = _file_hexdigest(self.path)
        except FileNotFoundError:
            return False
        return current_hash == self.identity

    @property
    def integrity_status(self):
        try:
            current_hash = _file_hexdigest(self.path)
        except FileNotFoundError:
            return "missing"
        if current_hash == self.identity:
            return "intact"
        return "modified"

    def check_integrity(self):
        return self.integrity_status

    def find_matching_files(self, search_location: Path):
        matching = []
        for candidate in search_location.rglob("*"):
            if candidate.is_file():
                try:
                    candidate_hash = _file_hexdigest(candidate)
                except (OSError, FileNotFoundError):
                    continue
                if candidate_hash == self.identity:
                    matching.append(candidate)
        return matching

    def verify_file(self, file_path: Path) -> bool:
        try:
            candidate_hash = _file_hexdigest(file_path)
        except (OSError, FileNotFoundError):
            return False
        return candidate_hash == self.identity

    def reassociate_file(self, file_path: Path) -> bool:
        if self.verify_file(file_path):
            self.path = file_path
            return True
        return False

    def set_order(self, n: int) -> None:
        self.order = n


class ArchivalObject:
    def __init__(self):
        self.representations = []

    def add_representation(self, path: Path, confirm_duplicate: bool = False):
        if self.check_for_duplicate(path):
            if confirm_duplicate:
                representation = Representation(
                    path=path,
                    duplicate=True,
                    added=True,
                )
                self.representations.append(representation)
                return representation
            else:
                return Representation(
                    path=path,
                    duplicate=True,
                    added=False,
                )

        representation = Representation(
            path=path,
            duplicate=False,
            added=True,
        )
        self.representations.append(representation)
        return representation

    def check_for_duplicate(self, path: Path) -> bool:
        candidate_hash = _file_digest(path)

        for representation in self.representations:
            if _file_digest(representation.path) == candidate_hash:
                return True

        return False

    @property
    def representations_needing_attention(self):
        return [
            rep
            for rep in self.representations
            if rep.integrity_status in ("modified", "missing")
        ]

    @property
    def ordered_representations(self):
        return sorted(
            [rep for rep in self.representations if rep.order is not None],
            key=lambda rep: rep.order,
        )


def create_archival_object():
    return ArchivalObject()
