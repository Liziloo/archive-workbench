from sqlmodel import Session
from app.db.session import engine
from app.services.adapters.digikam import DigiKamAdapter

def main():
    with Session(engine) as session:
        adapter = DigiKamAdapter(session)
        # We target our specific project
        adapter.reconcile_project("The Fifty Acres")

if __name__ == "__main__":
    main()