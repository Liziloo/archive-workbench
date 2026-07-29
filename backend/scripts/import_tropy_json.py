import os
from sqlmodel import Session
from app.db.session import engine
from app.services.adapters.tropy_json import TropyJsonAdapter

def main():
    # This path is now local to the GPU-Monster
    JSON_FILE = os.path.expanduser("~/GitHub/archive-workbench/tropy_export.json")

    if not os.path.exists(JSON_FILE):
        print(f"❌ Export file not found at {JSON_FILE}. Did you upload it?")
        return

    with Session(engine) as session:
        adapter = TropyJsonAdapter(JSON_FILE, session)
        adapter.reconcile()

if __name__ == "__main__":
    main()