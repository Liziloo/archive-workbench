import sqlite3

def discover():
    path = "/home/liz/project.tpy"
    print(f"🔍 Investigating Tropy Schema: {path}")

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    print("\n📋 Tables found in your Tropy file:")
    for table in tables:
        print(f" - {table}")
        # Show columns for the most likely candidates
        if table in ['item', 'items', 'photo', 'photos', 'metadata', 'values', 'properties']:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [c[1] for c in cursor.fetchall()]
            print(f"   Columns: {cols}")

    conn.close()

if __name__ == "__main__":
    discover()