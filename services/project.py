from sqlalchemy import select

from db import Session, Project
from schemas.project import ProjectCreate


async def get_projects(user_id: int):
    db = Session()
    query = select(Project).where(Project.user_id == user_id)
    projects = await db.execute(query)
    projects = projects.scalars().all()
    await db.close()
    return projects


async def create_project(user_id, project: ProjectCreate, image_url):
    db = Session()
    project_obj = Project(
        name=project.name,
        description=project.description,
        niche=project.niche,
        image_url=image_url,
        user_id=user_id
    )
    db.add(project_obj)
    await db.flush()
    await db.commit()
    return project_obj
