from fastapi import Body, FastAPI
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from archive_workbench.archival_object import ArchivalObject

app = FastAPI(title="Archive Workbench API")

# allow cross-origin requests for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for the first slice
_archival_objects = {
    "example-object": {
        "id": "example-object",
        "representations": [
            {"path": "letter-front.tif", "integrity_status": "intact"},
            {"path": "letter-back.tif", "integrity_status": "modified"},
        ],
    }
}


@app.get("/api/archival-objects/{object_id}")
async def get_archival_object(object_id: str):
    if object_id not in _archival_objects:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Object not found")
    return _archival_objects[object_id]


@app.post("/api/archival-objects/{object_id}/representations")
async def add_representation(object_id: str, path: str = Body(embed=True)):
    if object_id not in _archival_objects:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Object not found")

    # Create an ArchivalObject for processing
    archival_object = ArchivalObject()
    
    # Add all existing representations to the working object 
    existing_representations = _archival_objects[object_id]["representations"]
    for rep in existing_representations:
        try:
            rep_path = Path(rep["path"])
            # Add with confirm_duplicate=True so duplicate detection works properly
            archival_object.add_representation(rep_path, confirm_duplicate=True)
        except Exception:
            # Files may not exist in test scenarios - that's fine
            pass
    
    # Add the new representation using proper domain logic
    file_path = Path(path)
    representation_obj = archival_object.add_representation(file_path)
    
    # Build response with all current representations including the newly added one 
    final_representations = []
    for rep in archival_object.representations:
        final_representations.append({
            "path": str(rep.path),
            "integrity_status": rep.integrity_status,
        })
    
    # Update the in-memory store
    _archival_objects[object_id]["representations"] = final_representations
    
    return _archival_objects[object_id]
