from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, func
from app.db.session import engine
from app.models.core import Project, ArchivalItem
from typing import List, Dict, Any

router = APIRouter()

@router.get("/", response_model=List[Project])
def list_projects():
    """Returns a list of all available projects."""
    with Session(engine) as session:
        return session.exec(select(Project)).all()

@router.get("/{project_id}/stats")
def get_project_stats(project_id: str):
    """Returns counts of items and assets for a specific project."""
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        item_count = session.exec(
            select(func.count(ArchivalItem.id)).where(ArchivalItem.project_id == project_id)
        ).one()

        return {
            "name": project.name,
            "item_count": item_count,
            "config": project.config
        }