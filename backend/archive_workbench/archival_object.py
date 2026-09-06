from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone


class Representation:
    def __init__(self, path: Path, duplicate: bool, added: bool):
        self.path = path
        self.duplicate = duplicate
        self.added = added
        self.identity = sha256(path.read_bytes()).hexdigest()
        self.representation = self
        self.added_at = datetime.now(timezone.utc)

    def read_bytes(self):
        return self.path.read_bytes()

    def matches_current_file(self):
        try:
            current_hash = sha256(self.path.read_bytes()).hexdigest()
        except FileNotFoundError:
            return False
        return current_hash == self.identity

    @property
    def integrity_status(self):
        try:
            current_hash = sha256(self.path.read_bytes()).hexdigest()
        except FileNotFoundError:
            return "missing"
        if current_hash == self.identity:
            return "intact"
        return "modified"


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
        candidate_hash = sha256(path.read_bytes()).digest()

        for representation in self.representations:
            if sha256(representation.read_bytes()).digest() == candidate_hash:
                return True

        return False


def create_archival_object():
    return ArchivalObject()
