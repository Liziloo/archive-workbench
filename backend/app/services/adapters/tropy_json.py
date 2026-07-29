import json
import re
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

        items = data.get('@graph', [])
        stats = {"matched": 0, "missing": 0}

        for item in items:
            manual_id = item.get('identifier')
            if not manual_id:
                continue

            clean_id = str(manual_id).strip().zfill(4)

            # --- Extract the Note (Deep Nesting Fix) ---
            note_text = ""
            photos = item.get('photo', [])
            if photos and isinstance(photos, list):
                # We check the first photo's notes
                notes = photos[0].get('note', [])
                if notes and isinstance(notes, list):
                    # Tropy stores text in {'text': {'@value': '...'}}
                    text_wrapper = notes[0].get('text', {})
                    if isinstance(text_wrapper, dict):
                        note_text = text_wrapper.get('@value', '')

            # --- Extract other metadata ---
            metadata = {
                "tropy_title": item.get('title'),
                "tropy_description": item.get('description'),
                "tropy_subject": item.get('subject'),
                "tropy_date": item.get('date'),
                "tropy_tags": ", ".join(item.get('tag', [])) if item.get('tag') else None
            }

            # --- Surgical Match ---
            statement = select(DigitalAsset).where(DigitalAsset.file_path.contains(clean_id))
            potential_assets = self.session.exec(statement).all()
            pattern = rf"(?<!\d){clean_id}(?!\d)"
            valid_matches = [a for a in potential_assets if re.search(pattern, a.file_path)]

            if len(valid_matches) == 1:
                asset = valid_matches[0]

                # Add the Note
                if note_text:
                    self.session.add(EvidenceClaim(
                        item_id=asset.item_id, source_context="Tropy JSON Export",
                        property="historical_note", value=note_text
                    ))

                # Add Metadata
                for prop, val in metadata.items():
                    if val:
                        self.session.add(EvidenceClaim(
                            item_id=asset.item_id, source_context="Tropy JSON Export",
                            property=prop, value=str(val)
                        ))
                stats["matched"] += 1
            else:
                stats["missing"] += 1

        self.session.commit()
        print(f"✅ Tropy Import Complete. Matched: {stats['matched']} | Missing: {stats['missing']}")