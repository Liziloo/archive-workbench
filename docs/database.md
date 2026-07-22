**Purpose:** Explains *why* the database is built the way it is.
*   **Artifact-Centric:** One `ArchivalItem` can have many `DigitalAssets` (front scan, back scan, low-res reference).
*   **Evidence Claims:** Explain that we store *raw* data from Tropy/Immich separately from the *canonical* data we send to Omeka.
*   **JSONB Usage:** Explain that we use JSONB for `external_identifiers` so we can add new catalog IDs (like Carl's) without changing the database structure.
