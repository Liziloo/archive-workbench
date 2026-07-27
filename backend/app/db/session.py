from sqlmodel import create_engine, Session
from app.core.config import settings # Assuming a config for DATABASE_URL

engine = create_engine(
    settings.DATABASE_URL,
    echo=True, # Useful for debugging SQL during development
    json_serializer=lambda obj: obj # Let Postgres handle JSONB optimization
)

def get_session():
    with Session(engine) as session:
        yield session