import json
import re
import pathlib
from typing import List, Dict, Any
from sqlmodel import Session, select
from app.models.core import DigitalAsset, EvidenceClaim

class TropyJsonAdapter:
    def __init__(self, json_path: str, session: Session):
        self.json_path = json_path
        self.session = session

    def reconcile(self):
        print(f"📖 Reading Tropy JSON Export: {self.json_path}")
        with open(self.json_path, 'r') as f:
            data = json.load(f)

        # Tropy JSON-LD wraps everything in a '@graph' list
        items = data.get('@graph', [])

        stats = {"matched": 0, "missing": 0, "no_id": 0}

        for item in items:
            # 1. Extract the Identifier (your 4-digit ID)
            # Tropy usually uses 'dc:identifier' or 'identifier'
            manual_id = item.get('http://purl.org/dc/elements/1.1/identifier') or \
                        item.get('dc:identifier') or \
                        item.get('identifier')

            if not manual_id:
                stats["no_id"] += 1
                continue

            # Clean the ID (e.g., "42" -> "0042")
            clean_id = str(manual_id).strip().zfill(4)

            # 2. Extract the Note
            # Tropy notes are often objects in a list: "note": [{"text": "..."}]
            notes = item.get('note', [])
            note_text = ""
            if isinstance(notes, list) and len(notes) > 0:
                note_text = notes[0].get('text', '')
            elif isinstance(notes, str):
                note_text = notes

            # 3. Surgical Match in Postgres
            # We look for the ID surrounded by non-digits
            statement = select(DigitalAsset).where(DigitalAsset.file_path.contains(clean_id))
            potential_assets = self.session.exec(statement).all()

            pattern = rf"(?<!\d){clean_id}(?!\d)"
            valid_matches = [a for a in potential_assets if re.search(pattern, a.file_path)]

            if len(valid_matches) == 1:
                asset = valid_matches[0]

                # Record the Note as an EvidenceClaim
                if note_text:
                    self.session.add(EvidenceClaim(
                        item_id=asset.item_id,
                        source_context="Tropy JSON Export",
                        property="historical_note",
                        value=note_text,
                        is_verified=False
                    ))

                # Record the Legacy ID as an EvidenceClaim
                self.session.add(EvidenceClaim(
                    item_id=asset.item_id,
                    source_context="Tropy JSON Export",
                    property="legacy_id",
                    value=clean_id,
                    is_verified=True
                ))
                stats["matched"] += 1
            else:
                stats["missing"] += 1

        self.session.commit()
        print(f"\n✅ Tropy JSON Import Complete")
        print(f"   Matched:   {stats['matched']}")
        print(f"   Missing:   {stats['missing']} (ID found in Tropy but not on disk)")
        print(f"   No ID:     {stats['no_id']} (Items skipped because they had no Identifier)")