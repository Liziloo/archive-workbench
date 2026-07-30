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

class ProposedMatchStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

# --- Models ---

class Project(SQLModel, table=True):
    """A distinct archival collection with its own settings and paths."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None

    # This stores paths and settings specific to this archive
    # e.g., {"path_raw": "/home/liz/...", "tropy_id_field": "identifier"}
    config: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    items: List["ArchivalItem"] = Relationship(back_populates="project")

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

    visual_embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSONB))

    # Relationships
    item_id: Optional[UUID] = Field(default=None, foreign_key="archivalitem.id")
    item: Optional["ArchivalItem"] = Relationship(back_populates="digital_assets")

class EvidenceClaim(SQLModel, table=True):
    """Atomic data points extracted from sources (Tropy, XMP, AI)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    source_context: str
    property: str
    value: str
    is_verified: bool = Field(default=False)

    # Relationships
    item_id: UUID = Field(foreign_key="archivalitem.id")
    item: "ArchivalItem" = Relationship(back_populates="evidence_claims")

class AuthorityLink(SQLModel, table=True):
    """Links to external research (WikiTree, Obsidian, etc.)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    system_name: str
    system_id: str
    uri: Optional[str] = None

    # Relationships
    item_id: UUID = Field(foreign_key="archivalitem.id")
    item: "ArchivalItem" = Relationship(back_populates="authority_links")

class ArchivalItem(SQLModel, table=True):
    """The conceptual 'Object'. The parent of all assets and evidence."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: ItemStatus = Field(default=ItemStatus.DRAFT)

    # NEW: Link to the Project
    project_id: Optional[UUID] = Field(default=None, foreign_key="project.id")
    project: Optional[Project] = Relationship(back_populates="items")

    # Physical-to-Digital Hierarchy
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

class ProposedMatch(SQLModel, table=True):
    """Stores AI-suggested matches between two digital assets for human review."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # The two assets being compared
    asset_a_sha256: str = Field(foreign_key="digitalasset.sha256")
    asset_b_sha256: str = Field(foreign_key="digitalasset.sha256")

    # How similar the AI thinks they are (0.0 to 1.0)
    similarity_score: float

    status: ProposedMatchStatus = Field(default=ProposedMatchStatus.PENDING)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None