from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Curation staging area for The Fifty Acres archive",
    version="0.1.0"
)

# Set up CORS so the React frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our API routes (this pulls in the /system/status endpoint)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Archive Workbench API is online"}