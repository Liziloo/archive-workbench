import os
from sqlmodel import Session
from app.db.session import engine
from app.services.harvester import HarvesterService
from app.models.core import AssetRole

def main():
    # Define our sources based on the verified .env keys
    sources = [
        (os.getenv("PATH_RAW"), AssetRole.PRIMARY),
        (os.getenv("PATH_EDITED"), AssetRole.PRIMARY),
        (os.getenv("PATH_CARL"), AssetRole.REFERENCE),
    ]

    with Session(engine) as session:
        harvester = HarvesterService(session)

        for path, role in sources:
            if not path:
                print(f"⚠️  Skipping: No path defined for {role.value}")
                continue

            print(f"🚀 Ingesting {role.value} assets from: {path}")
            count = harvester.scan(path, role=role)
            print(f"✅ Finished {role.value}: {stats['new']} new assets registered.")

if __name__ == "__main__":
    main()