from sqlmodel import Session, select
from app.db.session import engine
from app.models.core import Project, ArchivalItem
from app.core.config import settings

def initialize():
    with Session(engine) as session:
        # 1. Check if the project already exists
        existing_project = session.exec(select(Project).where(Project.name == "The Fifty Acres")).first()

        if not existing_project:
            print("🚀 Creating 'The Fifty Acres' project...")
            project = Project(
                name="The Fifty Acres",
                description="Haushalter-Casler Family Archive curation project.",
                config={
                    "path_raw": settings.PATH_RAW,
                    "path_edited": settings.PATH_EDITED,
                    "path_carl": settings.PATH_CARL
                }
            )
            session.add(project)
            session.commit()
            session.refresh(project)
        else:
            project = existing_project
            print(f"ℹ️ Project '{project.name}' already exists.")

        # 2. Link orphaned items to this project
        orphans = session.exec(select(ArchivalItem).where(ArchivalItem.project_id == None)).all()
        if orphans:
            print(f"🔗 Linking {len(orphans)} orphaned items to project...")
            for item in orphans:
                item.project_id = project.id
                session.add(item)
            session.commit()
            print("✅ Items successfully linked.")
        else:
            print("✅ No orphaned items found.")

if __name__ == "__main__":
    initialize()