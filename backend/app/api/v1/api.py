from fastapi import APIRouter
from app.api.v1.endpoints import system, projects, matches

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])