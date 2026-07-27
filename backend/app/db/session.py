import json
from sqlmodel import create_engine, Session
from app.core.config import settings

# Remove the lambda obj: obj line.
# SQLAlchemy will now automatically handle the dict -> JSON conversion.
engine = create_engine(
    settings.DATABASE_URL,
    echo=False # Set to False to reduce terminal noise
)

def get_session():
    with Session(engine) as session:
        yield session