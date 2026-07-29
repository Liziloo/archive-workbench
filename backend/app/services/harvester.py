import hashlib
import pathlib
from typing import Optional
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

    def ingest_file(self, file_path: pathlib.Path, role: AssetRole):
        """Processes a single file with a specific archival role."""
        file_hash = self.calculate_sha256(file_path)

        # Level 1 Match: Check for existing hash
        statement = select(DigitalAsset).where(DigitalAsset.sha256 == file_hash)
        existing_asset = self.session.exec(statement).first()

        if existing_asset:
            # HEALING/DUPLICATION LOGIC:
            # If the exact same hash is found in a different folder:
            if existing_asset.file_path != str(file_path):
                # We don't create a new ArchivalItem.
                # For now, we just log that we found a duplicate of an existing asset.
                # In the future, we could add this as a 'Supporting' asset to the same item.
                print(f"  - Duplicate hash found for {file_path.name} (Already registered)")
            return existing_asset

        # NEW ASSET FLOW
        # 1. Create the ArchivalItem (The 'Shell')
        # We store the source zone in the physical_address JSONB
        new_item = ArchivalItem(
            physical_address={
                "source_zone": role.value,
                "original_path": str(file_path.parent),
                "ingested_filename": file_path.name
            }
        )
        self.session.add(new_item)
        self.session.flush() # Get the new_item.id

        # 2. Create the DigitalAsset
        new_asset = DigitalAsset(
            sha256=file_hash,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            mime_type=file_path.suffix.lower(),
            asset_role=role,
            verification=VerificationStatus.AUTO_CONFIRMED,
            item_id=new_item.id
        )
        self.session.add(new_asset)
        self.session.commit()
        self.session.refresh(new_asset)
        return new_asset

    def scan(self, target_path: str, role: AssetRole):
        root = pathlib.Path(target_path)
        valid_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}

        stats = {"new": 0, "skipped": 0, "healed": 0}

        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in valid_exts:
                try:
                    # We'll modify ingest_file to return a status string
                    status = self.ingest_file(path, role=role)
                    stats[status] += 1
                except Exception as e:
                    print(f"  ❌ Error ingesting {path.name}: {e}")
                    self.session.rollback()

        print(f"  📊 Results: {stats['new']} New, {stats['skipped']} Skipped, {stats['healed']} Healed")
        return stats["new"]