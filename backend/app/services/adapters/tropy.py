import sqlite3
import re
import pathlib
from typing import List, Dict, Any
from sqlmodel import Session, select
from app.models.core import DigitalAsset, EvidenceClaim

class TropyAdapter:
    def __init__(self, tropy_db_path: str, session: Session):
        self.tropy_path = tropy_db_path
        self.session = session

    def get_tropy_data(self) -> List[Dict[str, Any]]:
        """Extracts 4-digit IDs and Notes using the metadata_values table."""
        # We use 'uri' or 'name' to find the Identifier property
        conn = sqlite3.connect(self.tropy_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
        SELECT
            mv.text as manual_id,
            n.text as note_content
        FROM metadata_values mv
        JOIN properties p ON mv.property_id = p.id
        LEFT JOIN notes n ON mv.item_id = n.item_id
        WHERE (p.name LIKE '%identifier%' OR p.uri LIKE '%identifier%')
          AND mv.text IS NOT NULL;
        """
        try:
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            print(f"❌ Query failed: {e}")
            # Fallback: Let's see what properties DO exist
            cursor.execute("SELECT name, uri FROM properties LIMIT 10;")
            props = cursor.fetchall()
            print(f"Available properties in your DB: {[p[0] for p in props]}")
            return []
        finally:
            conn.close()

    def reconcile(self):
        print(f"📖 Extracting data from Tropy: {self.tropy_path}")
        tropy_items = self.get_tropy_data()

        if not tropy_items:
            print("⚠️ No data recovered. Check if Tropy is open (close it to unlock the DB).")
            return

        print(f"Found {len(tropy_items)} items. Matching via 4-digit IDs...")

        stats = {"matched": 0, "ambiguous": 0, "missing": 0}

        for t_item in tropy_items:
            raw_id = str(t_item['manual_id']).strip().zfill(4)
            note = t_item['note_content']

            # Surgical Match: 4-digit ID with digit boundaries
            statement = select(DigitalAsset).where(DigitalAsset.file_path.contains(raw_id))
            potential_assets = self.session.exec(statement).all()

            # Regex to ensure '0042' doesn't match '20042'
            pattern = rf"(?<!\d){raw_id}(?!\d)"
            valid_matches = [a for a in potential_assets if re.search(pattern, a.file_path)]

            if len(valid_matches) == 1:
                asset = valid_matches[0]
                # Create the Note Claim
                if note:
                    self.session.add(EvidenceClaim(
                        item_id=asset.item_id,
                        source_context="Tropy Legacy Catalog",
                        property="historical_note",
                        value=note,
                        is_verified=False
                    ))
                # Create the ID Claim
                self.session.add(EvidenceClaim(
                    item_id=asset.item_id,
                    source_context="Tropy Legacy Catalog",
                    property="legacy_id",
                    value=raw_id,
                    is_verified=True
                ))
                stats["matched"] += 1
            elif len(valid_matches) > 1:
                stats["ambiguous"] += 1
            else:
                stats["missing"] += 1

        self.session.commit()
        print(f"✅ Done. Matched: {stats['matched']} | Ambiguous: {stats['ambiguous']} | Missing: {stats['missing']}")