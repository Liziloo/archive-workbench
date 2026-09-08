from fastapi import Body, FastAPI
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

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

    file_path = Path(path)
    if file_path.exists():
        integrity_status = "intact"
    else:
        integrity_status = "missing"

    new_representation = {
        "path": str(file_path),
        "integrity_status": integrity_status,
    }
    _archival_objects[object_id]["representations"].append(new_representation)
    return _archival_objects[object_id]
