from sqlmodel import Session
from app.db.session import engine
from app.services.matchmaker import MatchmakerService

def main():
    with Session(engine) as session:
        service = MatchmakerService(session)
        # We start with a high threshold (90%) to find the obvious ones first
        service.generate_proposals(threshold=0.90)

if __name__ == "__main__":
    main()