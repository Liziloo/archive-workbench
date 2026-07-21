# Archive Workbench: Unified Master Roadmap

## Phase 1: Skeleton Application (Proving the Stack)
*Goal: Establish communication between your GPU Workstation and Proxmox.*
- [ ] **Backend:** Initialize FastAPI (Python) with a "Hello World" endpoint.
- [ ] **Database:** Connect FastAPI to the PostgreSQL instance on Proxmox.
- [ ] **Frontend:** Confirm Vite/React can fetch data from the Backend.
- [ ] **Infrastructure:** Confirm Redis is reachable for background tasks.
- **Result:** You have a dashboard that says "Connection Successful."

## Phase 2: Project & Environment Management
*Goal: Make the tool reusable and configurable.*
- [ ] **Project Schema:** Define settings for "The Fifty Acres" (Image Dir, Tropy Path, Omeka Credentials).
- [ ] **Environment Check:** UI indicator for ROCm/GPU status (is the 7800 XT detected?).
- **Result:** You can select the "Haushalter Casler Archive" project.

## Phase 3: The Harvester (Database & Ingestion)
*Goal: Move from "Files" to "Digital Assets" using Deterministic Integrity.*
- [ ] **The Real Data Model:** Deploy the `ArchivalItem`, `DigitalAsset`, and `EvidenceClaim` schema.
- [ ] **The Hash Crawler:** Implement the service that scans your local directories and assigns SHA-256 IDs.
- [ ] **Initial Importers:** Build the "Adapters" for Tropy (SQLite) and DigiKam (XMP).
- **Result:** The database is populated with "Digital Assets" linked to their first "Evidence Claims."

## Phase 4: The Matchmaker (Reconciliation & Validation)
*Goal: Solve the "Rescan Problem" and validate data.*
- [ ] **Level 1 Match:** Auto-link assets with identical hashes.
- [ ] **Level 2/3 Match:** Build the UI to review "Proposed" matches based on Sleeve IDs or Visual Similarity (ROCm).
- [ ] **Validation Engine:** Flag missing images, duplicate IDs, or orphaned sidecars.
- **Result:** Your high-res scans are now correctly linked to your legacy Tropy/Carl metadata.

## Phase 5: The Workbench (Curation & Relationships)
*Goal: Human-in-the-loop synthesis of evidence.*
- [ ] **Review Interface:** The "Major UI" showing Image + Metadata + Historical Notes.
- [ ] **Relationship Builder:** Link Items to People (WikiTree/Obsidian) and Places.
- [ ] **Marginalia Pipeline:** Link "Back-of-Photo" scans and run local OCR.
- **Result:** You have "Verified" archival records ready for description.

## Phase 6: The Synthesizer (AI Integration)
*Goal: Generate public-facing narratives from verified facts.*
- [ ] **Prompt Builder:** Logic to feed "Verified Claims" into the LLM.
- [ ] **AI Generation:** ROCm-accelerated drafting of descriptions and alt-text.
- [ ] **Editorial Review:** UI to Approve, Edit, or Reject AI-generated content.
- **Result:** Every item has a scholarly, public-facing description.

## Phase 7: The Bridge (Omeka S Integration)
*Goal: Publication and Verification.*
- [ ] **Omeka Client:** Map Workbench records to Dublin Core and push via API.
- [ ] **Media Uploader:** Push high-res files to the Omeka server.
- [ ] **Verification:** Compare the local database against the live Omeka site to ensure 1:1 parity.
- **Result:** The archive is live and verified.
