import hashlib
import pathlib
from typing import Dict
from sqlmodel import Session, select
from app.models.core import DigitalAsset, ArchivalItem, AssetRole, VerificationStatus

class HarvesterService:
    def __init__(self, session: Session):
        self.session = session

    def calculate_sha256(self, file_path: pathlib.Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(8192), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def ingest_file(self, file_path: pathlib.Path, role: AssetRole) -> str:
        """Processes a file and returns a status string: 'new', 'skipped', or 'healed'."""
        file_hash = self.calculate_sha256(file_path)

        statement = select(DigitalAsset).where(DigitalAsset.sha256 == file_hash)
        existing_asset = self.session.exec(statement).first()

        if existing_asset:
            # HEALING: If the hash is the same but the path changed
            if existing_asset.file_path != str(file_path):
                existing_asset.file_path = str(file_path)
                self.session.add(existing_asset)
                self.session.commit()
                return "healed"
            # DUPLICATE: Same hash, same path
            return "skipped"

        # NEW ASSET FLOW
        new_item = ArchivalItem(
            physical_address={
                "source_zone": role.value,
                "original_path": str(file_path.parent),
                "ingested_filename": file_path.name
            }
        )
        self.session.add(new_item)
        self.session.flush()

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
        return "new"

    def scan(self, target_path: str, role: AssetRole) -> Dict[str, int]:
        root = pathlib.Path(target_path)
        valid_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}

        stats = {"new": 0, "skipped": 0, "healed": 0}

        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in valid_exts:
                try:
                    # Now ingest_file returns a string key for our stats dict
                    status = self.ingest_file(path, role=role)
                    stats[status] += 1
                except Exception as e:
                    print(f"  ❌ Error ingesting {path.name}: {e}")
                    self.session.rollback()

        print(f"  📊 Results: {stats['new']} New, {stats['skipped']} Skipped, {stats['healed']} Healed")
        return stats