from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import engine
from app.models.core import ArchivalItem, DigitalAsset, ProposedMatch, ProposedMatchStatus
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.get("/pending")
def get_pending_matches():
    with Session(engine) as session:
        # We join to get the file paths for the frontend to display
        statement = select(ProposedMatch).where(ProposedMatch.status == ProposedMatchStatus.PENDING)
        proposals = session.exec(statement).all()

        results = []
        for p in proposals:
            asset_a = session.get(DigitalAsset, p.asset_a_sha256)
            asset_b = session.get(DigitalAsset, p.asset_b_sha256)
            results.append({
                "id": p.id,
                "score": round(p.similarity_score * 100, 1),
                "asset_a": {"sha256": asset_a.sha256, "filename": asset_a.file_path.split('/')[-1]},
                "asset_b": {"sha256": asset_b.sha256, "filename": asset_b.file_path.split('/')[-1]}
            })
        return results

@router.post("/{match_id}/confirm")
def confirm_match(match_id: UUID):
    with Session(engine) as session:
        proposal = session.get(ProposedMatch, match_id)
        if not proposal:
            raise HTTPException(status_code=404, detail="Proposal not found")

        # Asset A = Carl's (Reference), Asset B = Yours (Primary)
        carl_asset = session.get(DigitalAsset, proposal.asset_a_sha256)
        your_asset = session.get(DigitalAsset, proposal.asset_b_sha256)

        # 1. Move Carl's asset to YOUR item
        old_item_id = carl_asset.item_id
        carl_asset.item_id = your_asset.item_id

        # 2. Mark proposal as confirmed
        proposal.status = ProposedMatchStatus.CONFIRMED
        proposal.reviewed_at = datetime.utcnow()

        session.add(carl_asset)
        session.add(proposal)
        session.commit()

        # 3. Cleanup: Delete the empty shell item Carl's asset used to belong to
        # (Only if it has no other assets left)
        old_item = session.get(ArchivalItem, old_item_id)
        if old_item and len(old_item.digital_assets) == 0:
            session.delete(old_item)
            session.commit()

        return {"status": "success", "message": "Items merged successfully"}

@router.post("/{match_id}/reject")
def reject_match(match_id: UUID):
    with Session(engine) as session:
        proposal = session.get(ProposedMatch, match_id)
        proposal.status = ProposedMatchStatus.REJECTED
        proposal.reviewed_at = datetime.utcnow()
        session.add(proposal)
        session.commit()
        return {"status": "rejected"}