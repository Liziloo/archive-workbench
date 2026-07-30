import numpy as np
from sqlmodel import Session, select
from app.models.core import DigitalAsset, ProposedMatch, ProposedMatchStatus, AssetRole
from typing import List

class MatchmakerService:
    def __init__(self, session: Session):
        self.session = session

    def calculate_similarity(self, feat1: List[float], feat2: List[float]) -> float:
        """Calculate cosine similarity between two embedding vectors."""
        v1 = np.array(feat1)
        v2 = np.array(feat2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def generate_proposals(self, threshold: float = 0.85):
        print(f"🔍 Starting Matchmaker (Threshold: {threshold})...")

        # 1. Get all Carl's scans (Reference)
        carl_assets = self.session.exec(
            select(DigitalAsset).where(DigitalAsset.asset_role == AssetRole.REFERENCE)
        ).all()

        # 2. Get all Your scans (Primary)
        primary_assets = self.session.exec(
            select(DigitalAsset).where(DigitalAsset.asset_role == AssetRole.PRIMARY)
        ).all()

        print(f"Comparing {len(carl_assets)} reference scans against {len(primary_assets)} primary scans...")

        match_count = 0
        for carl in carl_assets:
            if not carl.visual_embedding: continue

            for primary in primary_assets:
                if not primary.visual_embedding: continue

                # Skip if a proposal already exists for this pair
                existing = self.session.exec(
                    select(ProposedMatch).where(
                        ProposedMatch.asset_a_sha256 == carl.sha256,
                        ProposedMatch.asset_b_sha256 == primary.sha256
                    )
                ).first()
                if existing: continue

                # Calculate score
                score = self.calculate_similarity(carl.visual_embedding, primary.visual_embedding)

                if score >= threshold:
                    # Create a proposal
                    proposal = ProposedMatch(
                        asset_a_sha256=carl.sha256,
                        asset_b_sha256=primary.sha256,
                        similarity_score=float(score),
                        status=ProposedMatchStatus.PENDING
                    )
                    self.session.add(proposal)
                    match_count += 1
                    print(f"  ✨ Proposed Match ({score:.2f}): {carl.file_path.split('/')[-1]} <-> {primary.file_path.split('/')[-1]}")

        self.session.commit()
        print(f"✅ Created {match_count} new match proposals.")