import hashlib
import pathlib
from typing import List
from sqlmodel import Session, select
from app.models.core import DigitalAsset, ArchivalItem, AssetRole, VerificationStatus

class HarvesterService:
    def __init__(self, session: Session):
        self.session = session

    # ... calculate_sha256 remains the same ...

    def ingest_file(self, file_path: pathlib.Path, role: AssetRole):
        file_hash = self.calculate_sha256(file_path)

        # Level 1 Match: Check for existing hash
        statement = select(DigitalAsset).where(DigitalAsset.sha256 == file_hash)
        existing_asset = self.session.exec(statement).first()

        if existing_asset:
            # If we find the exact same file in another folder,
            # we don't create a new item. We just log it.
            return existing_asset

        # NEW ASSET LOGIC
        # We create a new ArchivalItem for every unique hash we find
        new_item = ArchivalItem(
            physical_address={
                "source_zone": role.value,
                "original_folder": str(file_path.parent)
            }
        )
        self.session.add(new_item)
        self.session.flush()

        new_asset = DigitalAsset(
            sha256=file_hash,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            mime_type=file_path.suffix.lower(),
            asset_role=role, # <--- This is the key
            verification=VerificationStatus.AUTO_CONFIRMED,
            item_id=new_item.id
        )
        self.session.add(new_asset)
        self.session.commit()
        return new_asset

    def scan(self, target_path: str, role: AssetRole):
        root = pathlib.Path(target_path)
        if not root.exists():
            print(f"⚠️  Path does not exist: {target_path}")
            return 0

        valid_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}
        count = 0
        for path in root.rglob("*"):
            if path.suffix.lower() in valid_exts:
                self.ingest_file(path, role=role)
                count += 1
        return count