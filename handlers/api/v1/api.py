from fastapi import APIRouter

from handlers.api.v1.endpoints import (
    auth,
    user,
    project,
    message,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(message.router, prefix="/message", tags=["message"])
