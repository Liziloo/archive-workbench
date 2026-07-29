from sqlmodel import Session, select, func
from app.db.session import engine
from app.models.core import ArchivalItem, DigitalAsset, EvidenceClaim

def audit():
    with Session(engine) as session:
        # 1. High Level Stats
        item_count = session.exec(select(func.count(ArchivalItem.id))).one()
        claim_count = session.exec(select(func.count(EvidenceClaim.id))).one()
        asset_count = session.exec(select(func.count(DigitalAsset.sha256))).one()

        print("\n" + "="*70)
        print("📊 ARCHIVE WORKBENCH - EVIDENCE AUDIT")
        print("="*70)
        print(f"{'Total Archival Items:':<30} {item_count}")
        print(f"{'Total Digital Assets:':<30} {asset_count}")
        print(f"{'Total Evidence Claims:':<30} {claim_count}")
        print("-" * 70)

        # 2. Property Breakdown (How many notes, tags, etc?)
        print("📋 CLAIMS BY PROPERTY TYPE:")
        # We query the count of each property type
        statement = select(EvidenceClaim.property, func.count(EvidenceClaim.id)).group_by(EvidenceClaim.property)
        results = session.exec(statement).all()

        for prop, count in results:
            print(f" - {prop:<25} {count}")
        print("-" * 70)

        # 3. Deep Dive: Spot-check 3 items with notes
        print("🔍 DEEP DIVE: MATCHED RECORDS SPOT-CHECK")
        # Find items that have at least one 'historical_note'
        note_statement = select(EvidenceClaim).where(EvidenceClaim.property == "historical_note").limit(3)
        sample_claims = session.exec(note_statement).all()

        if not sample_claims:
            print("⚠️  No 'historical_note' claims found. Check the property names in the breakdown above.")

        for claim in sample_claims:
            item = session.get(ArchivalItem, claim.item_id)
            # Get the primary asset for this item
            asset = next((a for a in item.digital_assets if a.asset_role == "primary"), None)
            filename = asset.file_path.split('/')[-1] if asset else "No File"

            print(f"\n📄 ITEM ID: {item.id}")
            print(f"   📁 FILENAME: {filename}")

            # Pull ALL evidence for this specific item
            all_evidence = session.exec(select(EvidenceClaim).where(EvidenceClaim.item_id == item.id)).all()
            for ev in all_evidence:
                # Truncate long notes for the terminal
                val_display = (ev.value[:75] + '...') if len(ev.value) > 75 else ev.value
                print(f"   📜 [{ev.property:<15}] : {val_display}")

        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    audit()