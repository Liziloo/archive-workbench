from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB

# --- Enums ---

class AssetRole(str, Enum):
    PRIMARY = "primary"   # High-res scan
    REFERENCE = "reference" # Low-res/Carl's catalog proxy
    BACK = "back"         # Back of photo/document
    SUPPORTING = "supporting" # Contextual material

class VerificationStatus(str, Enum):
    AUTO_CONFIRMED = "auto_confirmed"
    PENDING = "pending"
    REJECTED = "rejected"
    VERIFIED = "verified"

class ItemStatus(str, Enum):
    DRAFT = "draft"
    VERIFIED = "verified"
    PUBLISHED = "published"

# --- Models ---

class DigitalAsset(SQLModel, table=True):
    """The physical file on disk. Deterministic identity via SHA-256."""
    sha256: str = Field(primary_key=True, index=True)
    file_path: str = Field(unique=True)
    file_size: int
    mime_type: str
    asset_role: AssetRole = Field(default=AssetRole.PRIMARY)
    verification: VerificationStatus = Field(default=VerificationStatus.PENDING)

    # Technical metadata (EXIF, resolution, etc.)
    technical_metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    # Relationships
    item_id: Optional[UUID] = Field(default=None, foreign_key="archivalitem.id")
    item: Optional["ArchivalItem"] = Relationship(back_populates="digital_assets")

class EvidenceClaim(SQLModel, table=True):
    """Atomic data points extracted from sources (Tropy, XMP, AI)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    source_context: str  # e.g., "Tropy-Export-2024", "DigiKam-XMP", "Ollama-VLM"
    property: str        # e.g., "date_created", "subject_person", "transcription"
    value: str
    is_verified: bool = Field(default=False)

    # Relationships
    item_id: UUID = Field(foreign_key="archivalitem.id")
    item: "ArchivalItem" = Relationship(back_populates="evidence_claims")

class AuthorityLink(SQLModel, table=True):
    """Links to external research (WikiTree, Obsidian, etc.)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    system_name: str # "WikiTree", "Obsidian"
    system_id: str   # The unique ID in that system
    uri: Optional[str] = None

    # Relationships
    item_id: UUID = Field(foreign_key="archivalitem.id")
    item: "ArchivalItem" = Relationship(back_populates="authority_links")

class ArchivalItem(SQLModel, table=True):
    """The conceptual 'Object'. The parent of all assets and evidence."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: ItemStatus = Field(default=ItemStatus.DRAFT)

    # Physical-to-Digital Hierarchy
    # Expected keys: series, box, folder, bin
    physical_address: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    # Legacy IDs from Tropy or Carl's Catalog
    external_identifiers: Dict[str, str] = Field(default_factory=dict, sa_column=Column(JSONB))

    # The final, curated Dublin Core metadata for Omeka S
    canonical_metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    # Relationships
    digital_assets: List[DigitalAsset] = Relationship(back_populates="item")
    evidence_claims: List[EvidenceClaim] = Relationship(back_populates="item")
    authority_links: List[AuthorityLink] = Relationship(back_populates="item")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)