from sqlmodel import Session, select, func
from app.db.session import engine
from app.models.core import ArchivalItem, DigitalAsset

def inspect():
    with Session(engine) as session:
        # 1. Count total records
        item_count = session.exec(select(func.count(ArchivalItem.id))).one()
        asset_count = session.exec(select(func.count(DigitalAsset.sha256))).one()

        print("\n" + "="*60)
        print("📊 ARCHIVE WORKBENCH - DATABASE STATUS")
        print("="*60)
        print(f"{'Conceptual Items:':<25} {item_count}")
        print(f"{'Digital Assets:':<25} {asset_count}")
        print("-" * 60)

        # 2. Show the last 5 ingested files
        print("📂 RECENTLY INGESTED ASSETS:")
        statement = select(DigitalAsset).order_by(DigitalAsset.sha256).limit(5)
        assets = session.exec(statement).all()

        if not assets:
            print("   (No assets found in database)")
        else:
            for asset in assets:
                # Truncate hash for readability
                short_hash = f"{asset.sha256[:8]}...{asset.sha256[-8:]}"
                filename = asset.file_path.split('/')[-1]
                print(f"   Fingerprint: {short_hash} | File: {filename}")

        print("="*60 + "\n")

if __name__ == "__main__":
    inspect()