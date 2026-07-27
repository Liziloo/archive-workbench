from app.db.session import engine
from app.services.harvester import HarvesterService
from app.core.config import settings
from sqlmodel import Session

def main():
    print(f"🚀 Starting Harvester on {settings.STAGING_DIRECTORY}")
    with Session(engine) as session:
        harvester = HarvesterService(session)
        count = harvester.scan(settings.STAGING_DIRECTORY)
    print(f"✅ Finished. Ingested/Verified {count} assets.")

if __name__ == "__main__":
    main()