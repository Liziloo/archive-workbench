from sqlmodel import SQLModel, create_engine
from app.core.config import settings
from app.models.core import DigitalAsset, ArchivalItem, EvidenceClaim, AuthorityLink

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    # This will reach out to the server and create the tables
    SQLModel.metadata.create_all(engine)
    print("✅ Database schema synchronized with server.")

if __name__ == "__main__":
    create_db_and_tables()