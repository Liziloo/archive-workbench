import xml.etree.ElementTree as ET
import pathlib
from typing import Dict, List
from sqlmodel import Session, select
from app.models.core import DigitalAsset, EvidenceClaim, Project

class DigiKamAdapter:
    def __init__(self, session: Session):
        self.session = session
        self.ns = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'xmp': 'http://ns.adobe.com/xap/1.0/',
            'digiKam': 'http://www.digikam.org/ns/1.0/',
            'mwg-rs': 'http://www.metadataworkinggroup.com/schemas/regions/',
            'rs': 'http://www.metadataworkinggroup.com/schemas/regions/'
        }

    def parse_xmp(self, xmp_path: pathlib.Path) -> Dict[str, List[str]]:
        try:
            tree = ET.parse(xmp_path)
            root = tree.getroot()
            data = {"tags": [], "people": []}
            for li in root.findall(".//digiKam:TagsList/rdf:Seq/rdf:li", self.ns):
                if li.text: data["tags"].append(li.text)
            for region in root.findall(".//mwg-rs:Regionlist/rdf:Bag/rdf:li", self.ns):
                name = region.get("{http://www.metadataworkinggroup.com/schemas/regions/}Name")
                if name: data["people"].append(name)
            return data
        except Exception as e:
            print(f"  ⚠️  Failed to parse XMP {xmp_path.name}: {e}")
            return {"tags": [], "people": []}

    def reconcile_project(self, project_name: str):
        project = self.session.exec(select(Project).where(Project.name == project_name)).first()
        if not project:
            print(f"❌ Project '{project_name}' not found.")
            return

        paths_to_scan = [project.config.get("path_raw"), project.config.get("path_edited")]

        for source_path in paths_to_scan:
            if not source_path: continue
            root = pathlib.Path(source_path)
            print(f"📸 Scanning: {root}")

            # Case-insensitive search for .xmp or .XMP
            xmp_files = [f for f in root.rglob("*") if f.suffix.lower() == ".xmp"]
            print(f"🔍 Found {len(xmp_files)} total XMP files on disk.")

            match_count = 0
            for xmp_path in xmp_files:
                # If file is 'photo.jpg.xmp', stem is 'photo.jpg'
                # If file is 'photo.xmp', stem is 'photo'
                target_filename = xmp_path.stem

                # Try to find the asset. We use endswith to be more precise than 'contains'
                statement = select(DigitalAsset).where(DigitalAsset.file_path.like(f"%/{target_filename}"))
                asset = self.session.exec(statement).first()

                if asset:
                    metadata = self.parse_xmp(xmp_path)
                    for person in set(metadata["people"]):
                        self.session.add(EvidenceClaim(
                            item_id=asset.item_id, source_context="DigiKam XMP",
                            property="subject_person", value=person
                        ))
                    for tag in set(metadata["tags"]):
                        self.session.add(EvidenceClaim(
                            item_id=asset.item_id, source_context="DigiKam XMP",
                            property="digikam_tag", value=tag
                        ))
                    match_count += 1
                else:
                    # DEBUG: Print the first few failures to see the naming mismatch
                    if match_count < 1:
                        print(f"  ❓ No match for XMP: {xmp_path.name} (Looking for asset ending in: {target_filename})")

            self.session.commit()
            print(f"✅ Linked {match_count} XMP sidecars in '{project_name}'.")