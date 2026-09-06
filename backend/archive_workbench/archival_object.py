from hashlib import sha256
from pathlib import Path


class AddRepresentationResult:
    def __init__(self, duplicate: bool, added: bool):
        self.duplicate = duplicate
        self.added = added


class ArchivalObject:
    def __init__(self):
        self.representations = []

    def add_representation(self, path: Path, confirm_duplicate: bool = False):
        if self.check_for_duplicate(path):
            if confirm_duplicate:
                self.representations.append(path)
                return AddRepresentationResult(duplicate=True, added=True)
            else:
                return AddRepresentationResult(duplicate=True, added=False)
        self.representations.append(path)
        return path

    def check_for_duplicate(self, path: Path) -> bool:
        candidate_hash = sha256(path.read_bytes()).digest()

        for representation in self.representations:
            if sha256(representation.read_bytes()).digest() == candidate_hash:
                return True

        return False


def create_archival_object():
    return ArchivalObject()
