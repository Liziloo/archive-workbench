from sqlmodel import Session
from app.db.session import engine
from app.services.adapters.tropy import TropyAdapter

def main():
    # The path you provided
    TROPY_FILE = "/home/liz/project.tpy"

    with Session(engine) as session:
        adapter = TropyAdapter(TROPY_FILE, session)
        adapter.reconcile()

if __name__ == "__main__":
    main()