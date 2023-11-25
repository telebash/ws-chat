from loguru import logger
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


async def get_project(id: int):
    db = Session()
    project = await db.get(Project, id)
    await db.close()
    return project


async def favourite_project(id: int, user_id: int):
    db = Session()
    project = await db.get(Project, id)
    if not project or project.user_id != user_id:
        return False
    result = not project.is_favourite
    project.is_favourite = result
    db.add(project)
    await db.commit()
    await db.refresh(project)
    await db.close()
    return result


async def update_logo_project(id: int, user_id: int, logo_url: str):
    db = Session()
    project = await db.get(Project, id)
    if not project or project.user_id != user_id:
        return False
    project.image_url = logo_url
    db.add(project)
    await db.commit()
    await db.close()
    return project


async def delete_project(id: int, user_id: int):
    db = Session()
    project = await db.get(Project, id)
    if not project or project.user_id != user_id:
        return False
    await db.delete(project)
    await db.commit()
    await db.close()
    return True


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
