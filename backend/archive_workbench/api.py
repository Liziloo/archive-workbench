from fastapi import FastAPI
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
