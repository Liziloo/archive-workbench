from hashlib import sha256
from pathlib import Path


class ArchivalObject:
    def __init__(self):
        self.representations = []

    def add_representation(self, path: Path):
        representation = path
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
