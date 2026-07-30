from sqlmodel import Session
from app.db.session import engine
from app.services.vision import VisionService

def main():
    with Session(engine) as session:
        # Add force_cpu=True here for the test
        service = VisionService(session, force_cpu=True)
        service.generate_embeddings_for_all()

if __name__ == "__main__":
    main()