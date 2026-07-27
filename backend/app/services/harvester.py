import hashlib
import pathlib
from typing import List
from sqlmodel import Session, select
from app.models.core import DigitalAsset, ArchivalItem, AssetRole, VerificationStatus

class HarvesterService:
    def __init__(self, session: Session):
        self.session = session

    def calculate_sha256(self, file_path: pathlib.Path) -> str:
        """Memory-efficient hashing for large archival TIFFs."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(8192), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def ingest_file(self, file_path: pathlib.Path):
        """Processes a single file: Hash -> Match -> Register."""
        file_hash = self.calculate_sha256(file_path)

        # Level 1 Match: Check for existing hash
        statement = select(DigitalAsset).where(DigitalAsset.sha256 == file_hash)
        existing_asset = self.session.exec(statement).first()

        if existing_asset:
            # HEALING: If the file moved on the GPU-Monster, update the path
            if existing_asset.file_path != str(file_path):
                existing_asset.file_path = str(file_path)
                self.session.add(existing_asset)
                self.session.commit()
            return existing_asset

        # NEW ASSET: Create the hierarchy
        # 1. Create a conceptual ArchivalItem (The 'Shell')
        new_item = ArchivalItem(
            physical_address={"inferred_from_path": str(file_path.parent)}
        )
        self.session.add(new_item)
        self.session.flush() # Populates new_item.id

        # 2. Create the DigitalAsset
        new_asset = DigitalAsset(
            sha256=file_hash,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            mime_type=file_path.suffix.lower(),
            asset_role=AssetRole.PRIMARY,
            verification=VerificationStatus.AUTO_CONFIRMED,
            item_id=new_item.id
        )
        self.session.add(new_asset)
        self.session.commit()
        self.session.refresh(new_asset)
        return new_asset

    def scan(self, target_path: str):
        """Recursive scan of the staging directory."""
        root = pathlib.Path(target_path)
        valid_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}

        count = 0
        for path in root.rglob("*"):
            if path.suffix.lower() in valid_exts:
                self.ingest_file(path)
                count += 1
        return count